from ctp_builder import stages


def test_default_filter():
    filter = stages.Filter()
    default_config = filter.render()
    assert default_config == \
'''<DicomFilter
    class="org.rsna.ctp.stdstages.DicomFilter"
    name="DicomFilter"
    quarantine="/data/quarantines/CTP1/DicomFilter/DicomFilter"
    root="/data/roots/CTP1/DicomFilter/DicomFilter"
    script="DicomFilter.script"/>'''


def test_filter_config_values():
    filter = stages.Filter(name="TestName",
                           script="TestScript.script",
                           quarantine="/test",
                           root="/test")
    config = filter.render()
    assert config == \
'''<DicomFilter
    class="org.rsna.ctp.stdstages.DicomFilter"
    name="TestName"
    quarantine="/test/TestName"
    root="/test/TestName"
    script="TestScript.script"/>'''
