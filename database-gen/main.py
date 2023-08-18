from src.package_updater import PackageUpdater


def main():
    PackageUpdater(database_uri=f'mysql+pymysql://stc:stc@localhost/stc',
                   target_folder='../server/src/persistence/schema/').create_or_update()


if __name__ == "__main__":
    main()
