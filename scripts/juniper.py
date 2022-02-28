def juniper_save(lists):
    for name, sublists in lists.items():
        for subname, ips in sublists.items():
            with open(f"juniper/greynoise_{name}_{subname}.txt", "wt") as file:
                file.write("\n".join(ips))