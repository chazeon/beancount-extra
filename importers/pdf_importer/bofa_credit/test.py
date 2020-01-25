from beancount.ingest import regression_pytest
import pathlib
from . import ChaseStatementPDFImporter

importer = ChaseStatementPDFImporter("Asset:US:BofA:Checking")
directory = pathlib.Path(__file__).parent / "sample"

@regression_pytest.with_importer(importer)
@regression_pytest.with_testdir(directory)
class TestImporter(regression_pytest.ImporterTestBase):
    pass