import pytest

import owslib
from owslib.wfs import WebFeatureService
from tests.utils import service_ok

# Verify schema document is retrieved when the DescribeFeatureType request returns
# an xsd:include instead of the actual document. For example:

# <xsd:schema xmlns:gml31="http://www.opengis.net/gml" ... targetNamespace="http://xmlns.geoscience.gov.au/mineraltenementml/1.0">
#    <xsd:include schemaLocation="http://schemas.geoscience.gov.au/MineralTenementML/1.0/mineraltenementml.xsd"/>
#</xsd:schema>

WFS_SERVICE_URL = 'https://sarigdata.pir.sa.gov.au/geoserver/wfs?request=GetCapabilities'


class TestOnline(object):
    """Class grouping online tests for the WFS get_schema method."""
    @pytest.mark.online
    @pytest.mark.skipif(not service_ok(WFS_SERVICE_URL),
                        reason="WFS service is unreachable")
    @pytest.mark.parametrize("wfs_version", ["1.1.0", "2.0.0"])
    def test_schema_result(self, wfs_version):
        """Test whether the output from get_schema is a wellformed dictionary when the DescribeFeatureType request returns an xsd:include."""
        wfs = WebFeatureService(WFS_SERVICE_URL, version=wfs_version)
        schema = wfs.get_schema('gsmlbh:Borehole')
        assert isinstance(schema, dict)

        assert 'properties' in schema or 'geometry' in schema

        if 'geometry' in schema:
            assert 'geometry_column' in schema

        if 'properties' in schema:
            assert isinstance(schema['properties'], dict)

        assert 'required' in schema
        assert isinstance(schema['required'], list)

