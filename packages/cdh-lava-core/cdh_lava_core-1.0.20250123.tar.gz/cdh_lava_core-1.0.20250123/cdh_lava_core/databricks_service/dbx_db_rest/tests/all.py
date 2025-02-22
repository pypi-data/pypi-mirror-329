def main() -> None:
    """
    Run all tests.
    """
    from cdh_lava_core.databricks_service.dbx_db_rest.tests.highlevel import TestHighLevelFeatures
    import unittest

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestHighLevelFeatures))
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == "__main__":
    main()
