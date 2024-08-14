from cli.dump_temp_folder.service import DumpFolder


if __name__ == "__main__":
    dumper = DumpFolder()
    dumper.upload_files()
