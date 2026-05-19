from src.tools import TOOL_SPECS


def test_tool_specs_tem_minimo_cinco_ferramentas():
    nomes = {tool["name"] for tool in TOOL_SPECS}
    assert len(nomes) >= 5
    assert "buscar_material_rag" in nomes
    assert "planejar_estudos" in nomes
