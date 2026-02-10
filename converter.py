# Conversion logic for INTERLIS model objects (CartoSymTranscoder style)
# Place your conversion functions/classes here

# Example: from model.core import Model
# def convert_model_to_target(model: Model):
#     ...

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from model.core import Model, Topic, Class
from model.attributes import Attribute
from model.types import TextType

# Création d'un type texte
text_type = TextType(kind="Text", max_length=255)

# Création d'un attribut
attr = Attribute(name="Name", type_=text_type, mandatory=True)

# Création d'une classe avec cet attribut
classe = Class(name="MetaElement", attributes=[attr])

# Création d'un topic avec la classe
topic = Topic(name="ModelData", classes=[classe])

# Création du modèle avec le topic (correction des arguments)
model = Model(
    name="IlisMeta16",
    documentation=[],
    ili_version="2.4",
    contracted=False,
    kind="NormalM",
    language="fr",
    at="http://models.interlis.ch",
    version="2022-10-10",
    no_incremental_transfer=True,
    charset_iana_name="UTF-8",
    xmlns="http://models.interlis.ch"
)

print(model)

def test_ilismeta16_manual_instantiation():
    from model.core import Model, Package, DocText, MetaElement
    from model.types import DomainType
    from model.expressions import Expression
    from model.constraints import Constraint
    # Exemple de DocText
    doc = DocText(name="Description", text="Modèle de test IlisMeta16.")
    # Exemple de MetaElement (abstrait, mais on simule une sous-classe)
    class DummyMetaElement(MetaElement):
        pass
    meta_elem = DummyMetaElement(name="MetaElem1", documentation=[doc])
