from ..base.core_base import CoreBase
from ..mixins.rdf import RDFGeneratorMixin, RDFNeo4jExport
from ..mixins.rdf.model_rdf_mixin import ModelRDFMixin
from ..mixins.temporal import TemporalViewMixin, TemporalMixin


class Base(CoreBase, ModelRDFMixin, RDFGeneratorMixin, RDFNeo4jExport, TemporalMixin, TemporalViewMixin):
    __abstract__ = True
