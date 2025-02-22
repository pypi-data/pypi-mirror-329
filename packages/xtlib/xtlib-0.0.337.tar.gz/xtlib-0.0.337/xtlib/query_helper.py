# query_helper.py: common code for job, node, and run helpers
from xtlib import console, utils

def print_report(lines, which, config, store, args, builder, was_exported, row_count, limiter, limiter_value):
    store_name = config.get("store")
    workspace = args["workspace"]
    console.print("{} on {}/{}:".format(which, store_name, workspace))

    # print common hyperparameters on top of report
    if utils.safe_value(args, "common") and builder.hp_set_formatter.hp_sets_processed:
        console.print("\nCommon hyperparameters:")
        for hp,value in builder.hp_set_formatter.hp_unchanged_dict.items():
            console.print("  {}: {}".format(hp, value))
        console.print("")

    if was_exported:
        console.print("")

        for line in lines:
            console.print(line)
    else:
        # console.print the report
        if row_count > 0:
            console.print("")

            # filter out leading blank lines
            if lines and lines[0] == "":
                lines = lines[1:]

            if lines and lines[0] == "":
                lines = lines[1:]

            for line in lines:
                console.print(line)

            if row_count > 1:
                
                if limiter:
                    avail_count = store.database.avail_row_count
                    avail_text = "available: {:,}, ".format(avail_count) if avail_count is not None else ""
                    console.print("total {} listed: {:} ({}limited by --{}={:})".format(which, row_count, avail_text, limiter, limiter_value))
                else:
                    console.print("total {} listed: {:}".format(which, row_count))
        else:
            console.print("no matching {} found".format(which))





