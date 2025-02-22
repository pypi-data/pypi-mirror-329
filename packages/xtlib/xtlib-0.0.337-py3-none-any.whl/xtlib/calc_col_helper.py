# calc_col_helper.py: support for evaluating calculated columns
import os
import time
from collections import defaultdict

from xtlib import utils
from xtlib import constants

class CalcColHelper():
    def __init__(self):
        self.skus = None
        self.vm_size_errors = defaultdict(int)

    def load_skus(self):
        started = time.time()
        #print("loading azure_prices.pt")

        dir = os.path.dirname(os.path.realpath(__file__))
        fn = dir + "/azure_prices.pt"
        
        # TBD: remove this reliance on PyTorch (xtlib should not depend on PyTorch or any specific ML framework)
        import torch
        skus = torch.load(fn)

        self.skus = skus

        # skus["ND12am_A100_v4"] = a100         # 1xa100 (80gb)  
        # skus["ND40rs_v2"] = 22.03             # 8xv100 (32GB)
        # skus["ND96asr_v4"] = 27.20            # 8xa100 (40gb)
        # skus["ND96amsr_A100_v4"] = 32.77      # 8xa100 (80gb)

    def sku_cost_per_hour(self, record, default_vm_size="", default_location=""):

        def fixup_singularity_vm_size(vm_size):
            '''
            singularity custom VM sizes:
                P100 (16GB): NC6_v2, NC12_v2, NC24_v2, NC24r_v2
                V100 (16GB): NC6_v3, NC12_v3, NC24_v3, NC24r_v3
                V100 (16 GB): ND5_v2g1, ND10_v2g1, ND20_v2g1, ND40_v2g1
                V100 (32 GB): ND5_v2, ND10_v2, ND20_v2, ND40_v2
                A100 (80GB): ND12am_A100_v4, ND24am_A100_v4, ND48am_A100_v4, ND96amr_A100_v4, ND96amrs_A100_v4
            '''
            factor = 1

            if vm_size and vm_size.startswith("AISupercomputer."):
                vm_size = vm_size[len("AISupercomputer."):]

            # translation table for singularity VM sizes
            sd = {
                # P100 (16GB)
                "NC6_v2": ("NC6s_v2", 1), 
                "NC12_v2": ("NC12s_v2", 1), 
                "NC24_v2": ("NC24s_v2", 1), 
                "NC24r_v2": ("NC24rs_v2", 1),

                # V100 (16GB)
                "NC6_v3": ("NC6s_v3", 1), 
                "NC12_v3": ("NC12s_v3", 1), 
                "NC24_v3": ("NC24s_v3", 1), 
                "NC24r_v3": ("NC24rs_v3", 1),

                # V100 (16GB)
                "ND5_v2g1": ("NC6s_v3", 1), 
                "ND10_v2g1": ("NC6s_v3", 2), 
                "ND20_v2g1": ("NC6s_v3", 4), 
                "ND40_v2g1": ("NC6s_v3", 8),

                # V100 (32GB)
                "ND5_v2": ("ND40rs_v2", 1/8), 
                "ND10_v2": ("ND40rs_v2", 2/8), 
                "ND20_v2": ("ND40rs_v2", 4/8), 
                "ND40_v2": ("ND40rs_v2", 8/8),

                # A100 (80GB)
                "ND12am_A100_v4": ("ND96amsr_A100_v4", 1/8), 
                "ND24am_A100_v4": ("ND96amsr_A100_v4", 2/8), 
                "ND48am_A100_v4": ("ND96amsr_A100_v4", 4/8), 
                "ND96amr_A100_v4": ("ND96amsr_A100_v4", 8/8),
                "ND96amrs_A100_v4": ("ND96amsr_A100_v4", 8/8),
            }

            if vm_size in sd:
                vm_size, factor = sd[vm_size]

            return vm_size, factor

        def get_unit_price(vm_size, low_pri, region, default_region):

            if not self.skus:
                self.load_skus()
            skus = self.skus

            if vm_size and vm_size.startswith("Standard_"):
                vm_size = vm_size[len("Standard_"):]

            vm_size, factor = fixup_singularity_vm_size(vm_size)

            if not vm_size:
                vm_size = "None"

            low_pri = "low" if low_pri else "hi"
            sku_key = "{}-{}".format(vm_size, low_pri)
            if sku_key not in skus:
                error_key = "{},{}".format(vm_size, low_pri)
                self.vm_size_errors[error_key] += 1
                return 0
            
            sku = skus[sku_key]

            # previously thought azure regions were inconsistent, but it turns they are not
            # if region not in sku:
            #     self.swap_region_parts(region)

            if region not in sku:
                region = default_region

            if region not in sku:
                error_key = "{},{},{}".format(vm_size, low_pri, region)
                self.vm_size_errors[error_key] += 1
                return 0

            cost = factor * sku[region]
            return cost

        sku = utils.safe_value(record, "vm_size")
        if not sku:
            sku = default_vm_size

        low_pri = utils.safe_value(record, "low_pri")
        if low_pri:
            low_pri = int(low_pri)
        else:
            sla = utils.safe_value(record, "sla")
            if not sla or sla == "premium":
                low_pri = 0
            else:
                low_pri = 1

        location = utils.safe_value(record, "location")
        if not location:
            # for now, we don't have access to location in the log file, so we'll assume eastus
            location = default_location

        cost = get_unit_price(sku, low_pri, location, default_location)
        return cost
        
    def swap_region_parts(self, region):

        modifiers = ["northcentral", "southcentral", "eastcentral", "westcentral", "southeast", "southwest", "northeast", "northwest", 
            "north", "south", "east", "west", "central"]
        
        for mod in modifiers:
            if region.startswith(mod):
                mod_len = len(mod)
                region = region[mod_len:] + mod
                break

            if region.endswith(mod):
                mod_len = len(mod)
                region = mod + region[:-mod_len]
                break

        return region

    def eval_calculated_exp(self, calculated_exp, record):

        if not "sku_cost_per_hour" in record:
            record["sku_cost_per_hour"] = self.sku_cost_per_hour
            record["record"] = record

        try:
            value = eval(calculated_exp, record)
        except Exception as ex:
            value = None
            msg = "ERROR during eval of calc_exp: {}, ex: {}".format(calculated_exp, ex)
            
        return value

    def get_error_report(self, lines):

        if self.vm_size_errors:
            lines.append("")
            ignored_runs = 0

            msg = "WARNING: cannot find pricing for the following VM SKUs, priority, location combinations:"
            lines.append(msg)
            lines.append("")

            for desc, count in self.vm_size_errors.items():
                parts = desc.split(",")
                if len(parts) == 2:
                    msg = "  {:20s} {:5s} (found in {:,} runs)".format(parts[0], parts[1], count)
                else:
                    msg = "  {:20s} {:5s} {:15s} (found in {:,} runs)".format(parts[0], parts[1], parts[2], count)

                lines.append(msg)
                ignored_runs += count

            msg = "WARNING: {:,} runs were ignored when calculating unit_price & total_cost".format(ignored_runs)
            lines.append(msg)

if __name__ == "__main__":
    helper = CalcColHelper()

    # test 1 - test a specific sku that is not working
    sku = "NC6_v3"
    record = {"vm_size": sku, "low_pri": 1, "location": "westus2"}
    unit_cost = helper.sku_cost_per_hour(record, default_location="eastus")
    print(" {}: {}".format(sku, unit_cost))
    
    # test 2(standard vm sizes)
    print("\nstandard vm_sizes")
    for sku in ["NC6_v3", "ND96amsr_A100_v4"]:
        record = {"vm_size": sku, "low_pri": 0, "location": "eastus"}
        unit_cost = helper.sku_cost_per_hour(record)
        print(" {}: {}".format(sku, unit_cost))

    # test 3 (singularity custom vm sizes)
    print("\nsingularity vm_sizes")
    for sku in [
        "NC6_v2", "NC12_v2", "NC24_v2", "NC24r_v2",
        "NC6_v3", "NC12_v3", "NC24_v3", "NC24r_v3",
        "ND5_v2g1", "ND10_v2g1", "ND20_v2g1", "ND40_v2g1",
        "ND5_v2", "ND10_v2", "ND20_v2", "ND40_v2",
        "ND12am_A100_v4", "ND24am_A100_v4", "ND48am_A100_v4", "ND96amr_A100_v4", "ND96amrs_A100_v4",
    ]:
        record = {"vm_size": sku, "low_pri": 0, "location": "eastus"}
        unit_cost = helper.sku_cost_per_hour(record)
        print("  {}: {}".format(sku, unit_cost))

    # test 3
    #record = {"vm_size": "Standard_NC6s_v3", "low_pri": 0, "location": "eastus"}
    # cost = helper.eval_calculated_exp("sku_cost_per_hour(record, default_vm_size='NC6s_v3', default_location='eastus')", record)
    # print("cost: {}".format(cost))



