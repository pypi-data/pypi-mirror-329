from __future__ import annotations

import datetime
from dataclasses import field
from enum import Enum
from pydantic import BaseModel, PlainSerializer
from typing import List, Optional, Annotated

Timestamp = Annotated[
    datetime.datetime, PlainSerializer(lambda v: v.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z', return_type=str)
]


class JwtAuth(BaseModel):
    access_token: str
    refresh_token: str
    id_token: str
    expires_in: int
    refresh_expires_in: int
    not_before_policy: int
    scope: str
    session_state: str
    token_type: str


class Image(BaseModel):
    id: int
    registry: str
    name: str
    version: str
    dialect: str
    driver_class: str
    jdbc_method: str
    default_port: int
    data_types: List[DataType] = field(default_factory=list)


class ImageBrief(BaseModel):
    id: int
    name: str
    version: str
    jdbc_method: str
    default: bool


class BannerMessage(BaseModel):
    id: int
    type: str
    link: Optional[str] = None
    link_text: Optional[str] = None
    display_start: Optional[Timestamp] = None
    display_end: Optional[Timestamp] = None


class CreateDatabase(BaseModel):
    name: str
    container_id: int
    is_public: bool
    is_schema_public: bool


class UpdateView(BaseModel):
    is_public: bool


class CreateContainer(BaseModel):
    name: str
    host: str
    image_id: int
    privileged_username: str
    privileged_password: str
    ui_host: Optional[str] = None
    ui_port: Optional[int] = None
    port: Optional[int] = None


class CreateUser(BaseModel):
    username: str
    email: str
    password: str


class UpdateUser(BaseModel):
    theme: str
    language: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    affiliation: Optional[str] = None
    orcid: Optional[str] = None


class UserBrief(BaseModel):
    id: str
    username: str
    name: Optional[str] = None
    orcid: Optional[str] = None
    qualified_name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None


class Container(BaseModel):
    id: int
    name: str
    internal_name: str
    host: str
    port: int
    image: Image
    ui_host: Optional[str] = None
    ui_port: Optional[int] = None


class ContainerBrief(BaseModel):
    id: int
    name: str
    image: ImageBrief
    internal_name: str
    running: Optional[bool] = None
    hash: Optional[str] = None


class ColumnBrief(BaseModel):
    id: int
    name: str
    database_id: int
    table_id: int
    internal_name: str
    type: ColumnType
    alias: Optional[str] = None


class TableBrief(BaseModel):
    id: int
    database_id: int
    name: str
    description: Optional[str] = None
    internal_name: str
    is_versioned: bool
    is_public: bool
    is_schema_public: bool
    owned_by: str


class UserAttributes(BaseModel):
    theme: str
    orcid: Optional[str] = None
    affiliation: Optional[str] = None


class User(BaseModel):
    id: str
    username: str
    attributes: UserAttributes
    qualified_name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    name: Optional[str] = None


class UpdateUserTheme(BaseModel):
    theme: str


class UpdateUserPassword(BaseModel):
    password: str


class AccessType(str, Enum):
    """
    Enumeration of database access.
    """
    READ = "read"
    """The user can read all data."""

    WRITE_OWN = "write_own"
    """The user can write into self-owned tables and read all data."""

    WRITE_ALL = "write_all"
    """The user can write in all tables and read all data."""


class ColumnType(str, Enum):
    """
    Enumeration of table column data types.
    """
    CHAR = "char"
    VARCHAR = "varchar"
    BINARY = "binary"
    VARBINARY = "varbinary"
    TINYBLOB = "tinyblob"
    TINYTEXT = "tinytext"
    TEXT = "text"
    BLOB = "blob"
    MEDIUMTEXT = "mediumtext"
    MEDIUMBLOB = "mediumblob"
    LONGTEXT = "longtext"
    LONGBLOB = "longblob"
    ENUM = "enum"
    SERIAL = "serial"
    SET = "set"
    BIT = "bit"
    TINYINT = "tinyint"
    BOOL = "bool"
    SMALLINT = "smallint"
    MEDIUMINT = "mediumint"
    INT = "int"
    BIGINT = "bigint"
    FLOAT = "float"
    DOUBLE = "double"
    DECIMAL = "decimal"
    DATE = "date"
    DATETIME = "datetime"
    TIMESTAMP = "timestamp"
    TIME = "time"
    YEAR = "year"


class Language(str, Enum):
    """
    Enumeration of languages.
    """
    AB = "ab"
    AA = "aa"
    AF = "af"
    AK = "ak"
    SQ = "sq"
    AM = "am"
    AR = "ar"
    AN = "an"
    HY = "hy"
    AS = "as"
    AV = "av"
    AE = "ae"
    AY = "ay"
    AZ = "az"
    BM = "bm"
    BA = "ba"
    EU = "eu"
    BE = "be"
    BN = "bn"
    BH = "bh"
    BI = "bi"
    BS = "bs"
    BR = "br"
    BG = "bg"
    MY = "my"
    CA = "ca"
    KM = "km"
    CH = "ch"
    CE = "ce"
    NY = "ny"
    ZH = "zh"
    CU = "cu"
    CV = "cv"
    KW = "kw"
    CO = "co"
    CR = "cr"
    HR = "hr"
    CS = "cs"
    DA = "da"
    DV = "dv"
    NL = "nl"
    DZ = "dz"
    EN = "en"
    EO = "eo"
    ET = "et"
    EE = "ee"
    FO = "fo"
    FJ = "fj"
    FI = "fi"
    FR = "fr"
    FF = "ff"
    GD = "gd"
    GL = "gl"
    LG = "lg"
    KA = "ka"
    DE = "de"
    KI = "ki"
    EL = "el"
    KL = "kl"
    GN = "gn"
    GU = "gu"
    HT = "ht"
    HA = "ha"
    HE = "he"
    HZ = "hz"
    HI = "hi"
    HO = "ho"
    HU = "hu"
    IS = "is"
    IO = "io"
    IG = "ig"
    ID = "id"
    IA = "ia"
    IE = "ie"
    IU = "iu"
    IK = "ik"
    GA = "ga"
    IT = "it"
    JA = "ja"
    JV = "jv"
    KN = "kn"
    KR = "kr"
    KS = "ks"
    KK = "kk"
    RW = "rw"
    KV = "kv"
    KG = "kg"
    KO = "ko"
    KJ = "kj"
    KU = "ku"
    KY = "ky"
    LO = "lo"
    LA = "la"
    LV = "lv"
    LB = "lb"
    LI = "li"
    LN = "ln"
    LT = "lt"
    LU = "lu"
    MK = "mk"
    MG = "mg"
    MS = "ms"
    ML = "ml"
    MT = "mt"
    GV = "gv"
    MI = "mi"
    MR = "mr"
    MH = "mh"
    RO = "ro"
    MN = "mn"
    NA = "na"
    NV = "nv"
    ND = "nd"
    NG = "ng"
    NE = "ne"
    SE = "se"
    NO = "no"
    NB = "nb"
    NN = "nn"
    II = "ii"
    OC = "oc"
    OJ = "oj"
    OR = "or"
    OM = "om"
    OS = "os"
    PI = "pi"
    PA = "pa"
    PS = "ps"
    FA = "fa"
    PL = "pl"
    PT = "pt"
    QU = "qu"
    RM = "rm"
    RN = "rn"
    RU = "ru"
    SM = "sm"
    SG = "sg"
    SA = "sa"
    SC = "sc"
    SR = "sr"
    SN = "sn"
    SD = "sd"
    SI = "si"
    SK = "sk"
    SL = "sl"
    SO = "so"
    ST = "st"
    NR = "nr"
    ES = "es"
    SU = "su"
    SW = "sw"
    SS = "ss"
    SV = "sv"
    TL = "tl"
    TY = "ty"
    TG = "tg"
    TA = "ta"
    TT = "tt"
    TE = "te"
    TH = "th"
    BO = "bo"
    TI = "ti"
    TO = "to"
    TS = "ts"
    TN = "tn"
    TR = "tr"
    TK = "tk"
    TW = "tw"
    UG = "ug"
    UK = "uk"
    UR = "ur"
    UZ = "uz"
    VE = "ve"
    VI = "vi"
    VO = "vo"
    WA = "wa"
    CY = "cy"
    FY = "fy"
    WO = "wo"
    XH = "xh"
    YI = "yi"
    YO = "yo"
    ZA = "za"
    ZU = "zu"


class DatabaseAccess(BaseModel):
    type: AccessType
    user: UserBrief


class CreateAccess(BaseModel):
    type: AccessType


class UpdateAccess(BaseModel):
    type: AccessType


class IdentifierTitle(BaseModel):
    """
    Title of an identifier. See external documentation: https://support.datacite.org/docs/datacite-metadata-schema-v44-mandatory-properties#3-title.
    """
    id: int
    title: str
    language: Optional[Language] = None
    type: Optional[TitleType] = None


class SaveIdentifierTitle(BaseModel):
    title: str
    language: Optional[Language] = None
    type: Optional[TitleType] = None


class IdentifierDescription(BaseModel):
    id: int
    description: str
    language: Optional[Language] = None
    type: Optional[DescriptionType] = None


class SaveIdentifierDescription(BaseModel):
    description: str
    language: Optional[Language] = None
    type: Optional[DescriptionType] = None


class IdentifierFunder(BaseModel):
    id: int
    funder_name: str
    funder_identifier: Optional[str] = None
    funder_identifier_type: Optional[str] = None
    scheme_uri: Optional[str] = None
    award_number: Optional[str] = None
    award_title: Optional[str] = None


class SaveIdentifierFunder(BaseModel):
    funder_name: str
    funder_identifier: Optional[str] = None
    funder_identifier_type: Optional[str] = None
    scheme_uri: Optional[str] = None
    award_number: Optional[str] = None
    award_title: Optional[str] = None


class License(BaseModel):
    identifier: str
    uri: str
    description: str


class OntologyBrief(BaseModel):
    id: int
    uri: str
    prefix: str
    sparql: bool
    rdf: bool
    uri_pattern: Optional[str] = None


class Tuple(BaseModel):
    data: dict


class TupleUpdate(BaseModel):
    data: dict
    keys: dict


class TupleDelete(BaseModel):
    keys: dict


class Import(BaseModel):
    location: str
    separator: str
    header: bool
    quote: Optional[str] = None
    line_termination: Optional[str] = None


class UpdateColumn(BaseModel):
    concept_uri: Optional[str] = None
    unit_uri: Optional[str] = None


class ModifyVisibility(BaseModel):
    is_public: bool
    is_schema_public: bool


class ModifyOwner(BaseModel):
    id: str


class CreateTable(BaseModel):
    name: str
    is_public: bool
    is_schema_public: bool
    constraints: CreateTableConstraints
    columns: List[CreateTableColumn] = field(default_factory=list)
    description: Optional[str] = None


class CreateTableColumn(BaseModel):
    name: str
    type: ColumnType
    null_allowed: bool
    description: Optional[str] = None
    concept_uri: Optional[str] = None
    unit_uri: Optional[str] = None
    index_length: Optional[int] = None
    size: Optional[int] = None
    d: Optional[int] = None
    enums: Optional[List[str]] = None
    sets: Optional[List[str]] = None


class CreateTableConstraints(BaseModel):
    uniques: List[List[str]] = field(default_factory=list)
    checks: List[str] = field(default_factory=list)
    primary_key: List[str] = field(default_factory=list)
    foreign_keys: List[CreateForeignKey] = field(default_factory=list)


class NameIdentifierSchemeType(str, Enum):
    """
    Enumeration of name identifier scheme types.
    """
    ORCID = "ORCID"
    ROR = "ROR"
    ISNI = "ISNI"
    GRID = "GRID"


class AffiliationIdentifierSchemeType(str, Enum):
    """
    Enumeration of affiliation identifier scheme types.
    """
    ROR = "ROR"
    ISNI = "ISNI"
    GRID = "GRID"


class Creator(BaseModel):
    id: int
    creator_name: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    affiliation: Optional[str] = None
    name_type: Optional[str] = None
    name_identifier: Optional[str] = None
    name_identifier_scheme: Optional[NameIdentifierSchemeType] = None
    name_identifier_scheme_uri: Optional[str] = None
    affiliation_identifier: Optional[str] = None
    affiliation_identifier_scheme: Optional[str] = None
    affiliation_identifier_scheme_uri: Optional[str] = None


class CreatorBrief(BaseModel):
    id: int
    creator_name: str
    affiliation: Optional[str] = None
    name_type: Optional[str] = None
    name_identifier: Optional[str] = None
    name_identifier_scheme: Optional[NameIdentifierSchemeType] = None
    affiliation_identifier: Optional[str] = None
    affiliation_identifier_scheme: Optional[str] = None


class CreateIdentifierCreator(BaseModel):
    creator_name: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    affiliation: Optional[str] = None
    name_type: Optional[str] = None
    name_identifier: Optional[str] = None
    name_identifier_scheme: Optional[str] = None
    name_identifier_scheme_uri: Optional[str] = None
    affiliation_identifier: Optional[str] = None
    affiliation_identifier_scheme: Optional[str] = None
    affiliation_identifier_scheme_uri: Optional[str] = None


class RelatedIdentifier(BaseModel):
    id: int
    value: str
    type: RelatedIdentifierType
    relation: RelatedIdentifierRelation


class SaveRelatedIdentifier(BaseModel):
    value: str
    type: RelatedIdentifierType
    relation: RelatedIdentifierRelation


class CreateIdentifier(BaseModel):
    database_id: int
    type: IdentifierType
    creators: List[CreateIdentifierCreator]
    publication_year: int
    publisher: str
    titles: List[SaveIdentifierTitle]
    descriptions: List[SaveIdentifierDescription]
    funders: Optional[List[SaveIdentifierFunder]] = field(default_factory=list)
    doi: Optional[str] = None
    language: Optional[str] = None
    licenses: Optional[List[License]] = field(default_factory=list)
    query_id: Optional[int] = None
    table_id: Optional[int] = None
    view_id: Optional[int] = None
    query: Optional[str] = None
    query_normalized: Optional[str] = None
    execution: Optional[str] = None
    related_identifiers: Optional[List[SaveRelatedIdentifier]] = field(default_factory=list)
    result_hash: Optional[str] = None
    result_number: Optional[int] = None
    publication_day: Optional[int] = None
    publication_month: Optional[int] = None


class Identifier(BaseModel):
    id: int
    database_id: int
    type: IdentifierType
    status: IdentifierStatusType
    publication_year: int
    publisher: str
    creators: List[Creator]
    titles: List[IdentifierTitle]
    descriptions: List[IdentifierDescription]
    owner: UserBrief
    funders: Optional[List[IdentifierFunder]] = field(default_factory=list)
    doi: Optional[str] = None
    language: Optional[str] = None
    licenses: Optional[List[License]] = field(default_factory=list)
    query_id: Optional[int] = None
    table_id: Optional[int] = None
    view_id: Optional[int] = None
    query: Optional[str] = None
    query_normalized: Optional[str] = None
    execution: Optional[str] = None
    related_identifiers: Optional[List[RelatedIdentifier]] = field(default_factory=list)
    result_hash: Optional[str] = None
    result_number: Optional[int] = None
    publication_day: Optional[int] = None
    publication_month: Optional[int] = None


class IdentifierBrief(BaseModel):
    id: int
    database_id: int
    type: IdentifierType
    owned_by: str
    status: IdentifierStatusType
    publication_year: int
    publisher: str
    titles: List[IdentifierTitle]
    doi: Optional[str] = None
    query_id: Optional[int] = None
    table_id: Optional[int] = None
    view_id: Optional[int] = None


class View(BaseModel):
    id: int
    database_id: int
    name: str
    query: str
    query_hash: str
    owner: UserBrief
    internal_name: str
    is_public: bool
    initial_view: bool
    columns: List[ViewColumn]
    identifiers: List[Identifier] = field(default_factory=list)


class CreateView(BaseModel):
    name: str
    query: str
    is_public: bool
    is_schema_public: bool


class ViewBrief(BaseModel):
    id: int
    database_id: int
    name: str
    internal_name: str
    is_public: bool
    is_schema_public: bool
    initial_view: bool
    query: str
    query_hash: str
    owner: UserBrief


class ConceptBrief(BaseModel):
    id: int
    uri: str
    name: Optional[str] = None
    description: Optional[str] = None


class DatatypeAnalysis(BaseModel):
    separator: str
    columns: dict[str, ColumnType]
    line_termination: Optional[str] = None


class KeyAnalysis(BaseModel):
    keys: dict[str, int]


class ColumnStatistic(BaseModel):
    val_min: float
    val_max: float
    mean: float
    median: float
    std_dev: float


class ApiError(BaseModel):
    status: str
    message: str
    code: str


class TableStatistics(BaseModel):
    columns: dict[str, ColumnStatistic]


class UnitBrief(BaseModel):
    id: int
    uri: str
    name: Optional[str] = None
    description: Optional[str] = None


class ExecuteQuery(BaseModel):
    statement: str


class TitleType(str, Enum):
    """
    Enumeration of identifier title types.
    """
    ALTERNATIVE_TITLE = "AlternativeTitle"
    SUBTITLE = "Subtitle"
    TRANSLATED_TITLE = "TranslatedTitle"
    OTHER = "Other"


class RelatedIdentifierType(str, Enum):
    """
    Enumeration of related identifier types.
    """
    DOI = "DOI"
    URL = "URL"
    URN = "URN"
    ARK = "ARK"
    ARXIV = "arXiv"
    BIBCODE = "bibcode"
    EAN13 = "EAN13"
    EISSN = "EISSN"
    HANDLE = "Handle"
    IGSN = "IGSN"
    ISBN = "ISBN"
    ISTC = "ISTC"
    LISSN = "LISSN"
    LSID = "LSID"
    PMID = "PMID"
    PURL = "PURL"
    UPC = "UPC"
    W3ID = "w3id"


class RelatedIdentifierRelation(str, Enum):
    """
    Enumeration of related identifier types.
    """
    IS_CITED_BY = "IsCitedBy"
    CITES = "Cites"
    IS_SUPPLEMENT_TO = "IsSupplementTo"
    IS_SUPPLEMENTED_BY = "IsSupplementedBy"
    IS_CONTINUED_BY = "IsContinuedBy"
    CONTINUES = "Continues"
    IS_DESCRIBED_BY = "IsDescribedBy"
    DESCRIBES = "Describes"
    HAS_METADATA = "HasMetadata"
    IS_METADATA_FOR = "IsMetadataFor"
    HAS_VERSION = "HasVersion"
    IS_VERSION_OF = "IsVersionOf"
    IS_NEW_VERSION_OF = "IsNewVersionOf"
    IS_PREVIOUS_VERSION_OF = "IsPreviousVersionOf"
    IS_PART_OF = "IsPartOf"
    HAS_PART = "HasPart"
    IS_PUBLISHED_IN = "IsPublishedIn"
    IS_REFERENCED_BY = "IsReferencedBy"
    REFERENCES = "References"
    IS_DOCUMENTED_BY = "IsDocumentedBy"
    DOCUMENTS = "Documents"
    IS_COMPILED_BY = "IsCompiledBy"
    COMPILES = "Compiles"
    IS_VARIANT_FORM_OF = "IsVariantFormOf"
    IS_ORIGINAL_FORM_OF = "IsOriginalFormOf"
    IS_IDENTICAL_TO = "IsIdenticalTo"
    IS_REVIEWED_BY = "IsReviewedBy"
    REVIEWS = "Reviews"
    IS_DERIVED_FROM = "IsDerivedFrom"
    IS_SOURCE_OF = "IsSourceOf"
    IS_REQUIRED_BY = "IsRequiredBy"
    REQUIRES = "Requires"
    IS_OBSOLETED_BY = "IsObsoletedBy"
    OBSOLETES = "Obsoletes"


class DescriptionType(str, Enum):
    """
    Enumeration of identifier description types.
    """
    ABSTRACT = "Abstract"
    METHODS = "Methods"
    SERIES_INFORMATION = "SeriesInformation"
    TABLE_OF_CONTENTS = "TableOfContents"
    TECHNICAL_INFO = "TechnicalInfo"
    OTHER = "Other"


class QueryType(str, Enum):
    """
    Enumeration of query types.
    """
    VIEW = "view"
    """The query was executed as part of a view."""

    QUERY = "query"
    """The query was executed as subset."""


class IdentifierType(str, Enum):
    """
    Enumeration of identifier types.
    """
    VIEW = "view"
    """The identifier is identifying a view."""

    SUBSET = "subset"
    """The identifier is identifying a subset."""

    DATABASE = "database"
    """The identifier is identifying a database."""

    TABLE = "table"
    """The identifier is identifying a table."""


class IdentifierStatusType(str, Enum):
    """
    Enumeration of identifier status types.
    """
    PUBLISHED = "published"
    """The identifier is published and immutable."""

    DRAFT = "draft"
    """The identifier is a draft and can still be edited."""


class IdentifierType(str, Enum):
    """
    Enumeration of identifier types.
    """
    TABLE = "table"
    """The identifier identifies a table."""

    DATABASE = "database"
    """The identifier identifies a database."""

    VIEW = "view"
    """The identifier identifies a view."""

    SUBSET = "subset"
    """The identifier identifies a subset."""


class Query(BaseModel):
    id: int
    owner: UserBrief
    execution: Timestamp
    query: str
    type: QueryType
    database_id: int
    query_hash: str
    is_persisted: bool
    result_hash: str
    query_normalized: str
    result_number: Optional[int] = None
    identifiers: List[IdentifierBrief] = field(default_factory=list)


class UpdateQuery(BaseModel):
    persist: bool


class DataType(BaseModel):
    display_name: str
    value: str
    documentation: str
    is_quoted: bool
    is_buildable: bool
    size_min: Optional[int] = None
    size_max: Optional[int] = None
    size_default: Optional[int] = None
    size_required: Optional[bool] = None
    d_min: Optional[int] = None
    d_max: Optional[int] = None
    d_default: Optional[int] = None
    d_required: Optional[bool] = None
    data_hint: Optional[str] = None
    type_hint: Optional[str] = None


class Column(BaseModel):
    id: int
    name: str
    database_id: int
    table_id: int
    ord: int
    internal_name: str
    is_null_allowed: bool
    type: ColumnType
    alias: Optional[str] = None
    description: Optional[str] = None
    size: Optional[int] = None
    d: Optional[int] = None
    mean: Optional[float] = None
    median: Optional[float] = None
    concept: Optional[ConceptBrief] = None
    unit: Optional[UnitBrief] = None
    enums: Optional[List[str]] = field(default_factory=list)
    sets: Optional[List[str]] = field(default_factory=list)
    index_length: Optional[int] = None
    length: Optional[int] = None
    data_length: Optional[int] = None
    max_data_length: Optional[int] = None
    num_rows: Optional[int] = None
    val_min: Optional[float] = None
    val_max: Optional[float] = None
    std_dev: Optional[float] = None


class ViewColumn(BaseModel):
    id: int
    name: str
    database_id: int
    internal_name: str
    type: ColumnType
    is_null_allowed: bool
    alias: Optional[str] = None
    size: Optional[int] = None
    d: Optional[int] = None
    mean: Optional[float] = None
    median: Optional[float] = None
    concept: Optional[ConceptBrief] = None
    unit: Optional[UnitBrief] = None
    index_length: Optional[int] = None
    length: Optional[int] = None


class Table(BaseModel):
    id: int
    database_id: int
    name: str
    owner: UserBrief
    columns: List[Column]
    constraints: Constraints
    internal_name: str
    is_versioned: bool
    queue_name: str
    routing_key: str
    is_public: bool
    is_schema_public: bool
    identifiers: Optional[List[Identifier]] = field(default_factory=list)
    description: Optional[str] = None
    queue_type: Optional[str] = None
    num_rows: Optional[int] = None
    data_length: Optional[int] = None
    max_data_length: Optional[int] = None
    avg_row_length: Optional[int] = None


class DatabaseBrief(BaseModel):
    id: int
    name: str
    contact: UserBrief
    owner_id: str
    internal_name: str
    is_public: bool
    is_schema_public: bool
    identifiers: Optional[List[IdentifierBrief]] = field(default_factory=list)
    preview_image: Optional[str] = None
    description: Optional[str] = None


class Database(BaseModel):
    id: int
    name: str
    owner: UserBrief
    contact: UserBrief
    exchange_name: str
    internal_name: str
    is_public: bool
    is_schema_public: bool
    container: ContainerBrief
    identifiers: Optional[List[Identifier]] = field(default_factory=list)
    subsets: Optional[List[Identifier]] = field(default_factory=list)
    preview_image: Optional[str] = None
    description: Optional[str] = None
    tables: Optional[List[Table]] = field(default_factory=list)
    views: Optional[List[ViewBrief]] = field(default_factory=list)
    accesses: Optional[List[DatabaseAccess]] = field(default_factory=list)
    exchange_name: Optional[str] = None


class Unique(BaseModel):
    id: int
    table: TableBrief
    columns: List[ColumnBrief]


class ForeignKeyReference(BaseModel):
    id: int
    foreign_key: ForeignKeyBrief
    column: ColumnBrief
    referenced_column: ColumnBrief


class ReferenceType(str, Enum):
    """
    Enumeration of reference types.
    """
    RESTRICT = "restrict"
    CASCADE = "cascade"
    SET_NULL = "set_null"
    NO_ACTION = "no_action"
    SET_DEFAULT = "set_default"


class ForeignKeyBrief(BaseModel):
    id: int


class ForeignKey(BaseModel):
    id: int
    name: str
    references: List[ForeignKeyReference]
    table: TableBrief
    referenced_table: TableBrief
    on_update: Optional[ReferenceType] = None
    on_delete: Optional[ReferenceType] = None


class CreateForeignKey(BaseModel):
    columns: List[str]
    referenced_table: str
    referenced_columns: List[str]
    on_update: Optional[ReferenceType] = None
    on_delete: Optional[ReferenceType] = None


class PrimaryKey(BaseModel):
    id: int
    table: TableBrief
    column: ColumnBrief


class Constraints(BaseModel):
    uniques: List[Unique]
    foreign_keys: List[ForeignKey]
    checks: List[str]
    primary_key: List[PrimaryKey]
