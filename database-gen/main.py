from src.package_updater import PackageUpdater


def main():
    PackageUpdater(database_uri='sqlite:///../server/instance/dev.db',
                   target_folder='../server/src/persistence/schema/').create_or_update()


if __name__ == "__main__":
    main()
