"""Response and request models for the v1 API. Every field is described for /docs."""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

Clase = Literal["bajo", "medio", "alto"]
MES_EXAMPLE = "2026-09"


class ErrorBody(BaseModel):
    code: str = Field(
        description="Codigo estable: month_not_found, zone_not_found, model_not_loaded..."
    )
    message: str = Field(description="Detalle legible para depuracion.")


class ErrorResponse(BaseModel):
    error: ErrorBody


class ModelosEstado(BaseModel):
    clasificador: bool = Field(description="True si selected_model.joblib cargo sin error.")
    agente: bool = Field(description="True si el agente PPO esta disponible (hoy: no).")
    clusters: bool = Field(description="True si clusters.json esta publicado.")


class Health(BaseModel):
    status: Literal["ok"] = Field(description="Liveness del servicio.")
    modelos: ModelosEstado
    version: str = Field(description="Version de la API.", examples=["0.2.0"])


class Municipio(BaseModel):
    divipola: str = Field(description="Codigo DIVIPOLA de 5 digitos.", examples=["68001"])
    nombre: str = Field(description="Nombre oficial del municipio.", examples=["Bucaramanga"])
    lat: float = Field(description="Latitud del centroide municipal (WGS84).")
    lon: float = Field(description="Longitud del centroide municipal (WGS84).")
    poblacion: int | None = Field(description="Poblacion DANE (proyeccion CNPV 2018), o null.")


class PanelFila(BaseModel):
    divipola: str = Field(description="Codigo DIVIPOLA.")
    nombre: str = Field(description="Nombre del municipio.")
    features: dict[str, float | None] = Field(
        description="Variables de entrada del modelo al corte del mes (null si faltan)."
    )
    clase_observada: Clase | None = Field(description="Clase de riesgo observada en este mes.")
    target_clase_mes_siguiente: Clase | None = Field(
        description="Clase real del mes siguiente (objetivo de evaluacion)."
    )
    target_actividad_m3: int | None = Field(
        description="1 si hubo al menos un evento de magnitud >= 3 en los 3 meses siguientes."
    )


class Panel(BaseModel):
    mes: str = Field(description="Mes del panel (YYYY-MM).", examples=[MES_EXAMPLE])
    filas: list[PanelFila] = Field(description="Una fila por municipio.")


class ClasificarRequest(BaseModel):
    divipola: str = Field(description="Codigo DIVIPOLA del municipio.", examples=["68001"])
    mes: str = Field(
        pattern=r"^\d{4}-(0[1-9]|1[0-2])$",
        description="Mes a clasificar (YYYY-MM).",
        examples=[MES_EXAMPLE],
    )
    model_config = ConfigDict(
        json_schema_extra={"example": {"divipola": "68001", "mes": MES_EXAMPLE}}
    )


class Clasificacion(BaseModel):
    divipola: str = Field(description="Codigo DIVIPOLA.")
    mes: str = Field(description="Mes clasificado (YYYY-MM).")
    clase: Clase = Field(description="Clase de mayor probabilidad.")
    probabilidades: dict[Clase, float] = Field(description="Probabilidad por clase; suma 1.")
    modelo: str = Field(description="Archivo del modelo que produjo la clasificacion.")
    version: str = Field(description="Hash SHA-256 truncado del archivo del modelo.")
    exploratorio: Literal[True] = Field(description="Siempre true: no es alerta oficial.")


class PriorizacionMunicipio(BaseModel):
    divipola: str = Field(description="Codigo DIVIPOLA.")
    nombre: str = Field(description="Nombre del municipio.")
    rank: int = Field(description="Posicion dentro del metodo (1 = mas prioritario).", ge=1)


class MetodoPriorizacion(BaseModel):
    metodo: Literal["ppo", "estatico", "aleatorio"] = Field(
        description="Metodo que elige los municipios."
    )
    municipios: list[PriorizacionMunicipio] = Field(
        description="Top-k del metodo; vacio si no disponible."
    )
    recompensa_real: float | None = Field(
        description="Recompensa en el mes siguiente; null si no se evalua."
    )


class Priorizacion(BaseModel):
    corte: str = Field(description="Mes de corte (YYYY-MM).", examples=[MES_EXAMPLE])
    k: int = Field(description="Numero de municipios por metodo.", ge=1, le=87)
    exploratorio: Literal[True] = Field(description="Siempre true: priorizacion exploratoria.")
    nota: str = Field(description="Estado de cada metodo y advertencias de uso.")
    metodos: list[MetodoPriorizacion]


class Clusters(BaseModel):
    k: int = Field(description="Numero de grupos.")
    silhouette: float = Field(description="Silhouette del clustering.")
    grupos: list[dict[str, Any]] = Field(description="Etiqueta y descripcion de cada grupo.")
    municipios: list[dict[str, Any]] = Field(description="Municipio con su grupo asignado.")
