import json
import os
from copy import deepcopy
from pathlib import Path

import pytest
import requests
from dirty_equals import HasLen, HasAttributes, IsList, IsPartialDict
from pymultirole_plugins.v1.schema import Document, DocumentList

from pyprocessors_openai_completion.openai_completion import (
    OpenAICompletionProcessor,
    OpenAICompletionParameters,
    OpenAIModel,
    flatten_document, OpenAIFunction, AzureOpenAICompletionProcessor, ApolloOpenAICompletionProcessor,
    DeepInfraOpenAICompletionProcessor, AzureOpenAICompletionParameters, ApolloOpenAICompletionParameters,
    CHAT_GPT_MODEL_ENUM, DeepInfraOpenAICompletionParameters
)


def test_openai_completion_basic():
    model = OpenAICompletionProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == OpenAICompletionParameters

    model = AzureOpenAICompletionProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == AzureOpenAICompletionParameters

    model = DeepInfraOpenAICompletionProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == DeepInfraOpenAICompletionParameters

    model = ApolloOpenAICompletionProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == ApolloOpenAICompletionParameters


def test_flatten_doc():
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/complexdoc.json",
    )
    with source.open("r") as fin:
        jdoc = json.load(fin)
        doc = Document(**jdoc)
        flatten = flatten_document(doc)
        assert flatten == IsPartialDict(
            text=doc.text,
            title=doc.title,
            metadata_foo=doc.metadata["foo"],
            altTexts_0_name=doc.altTexts[0].name,
        )


JINJA_PROMPTS = {
    "preserve_entities": """Generates several variants of the following context while preserving the given named entities. Each named entity must be between square brackets using the notation [label:entity].
    Context: {{ doc.text }}
    {%- set entities=[] -%}
    {%- for a in doc.annotations -%}
      {%- do entities.append('[' + a.label + ':' + a.text + ']') -%}
    {%- endfor %}
    Given named entities using the notation [label:entity]: {{ entities|join(', ') }}
    Output language: {{ doc.metadata['language'] }}
    Output format: bullet list""",
    "substitute_entities": """Generates several variants of the following context while substituting the given named entities by semantically similar named entities with the same label, for each variant insert the new named entities between square brackets using the notation [label:entity].
    Context: {{ doc.text }}
    {%- set entities=[] -%}
    {%- for a in doc.annotations -%}
      {%- do entities.append('[' + a.label + ':' + a.text + ']') -%}
    {%- endfor %}
    Given named entities using the notation [label:entity]: {{ entities|join(', ') }}
    Output language: {{ doc.metadata['language'] }}
    Output format: bullet list""",
}


@pytest.mark.skip(reason="Not a test")
@pytest.mark.parametrize("typed_prompt", [p for p in JINJA_PROMPTS.items()])
def test_jinja_doc(typed_prompt):
    type = typed_prompt[0]
    prompt = typed_prompt[1]
    parameters = OpenAICompletionParameters(
        max_tokens=3000,
        completion_altText=type,
        prompt=prompt,
    )
    processor = OpenAICompletionProcessor()
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/jinjadocs.json",
    )
    with source.open("r") as fin:
        jdocs = json.load(fin)
        docs = [Document(**jdoc) for jdoc in jdocs]
        docs = processor.process(docs, parameters)
        assert docs == HasLen(6)
        sum_file = testdir / f"data/jinjadocs_{type}.json"
        dl = DocumentList(__root__=docs)
        with sum_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
    # noqa: E501


def chunks(seq, size=1000):  # noqa
    return (seq[pos: pos + size] for pos in range(0, len(seq), size))


@pytest.mark.skip(reason="Not a test")
def test_semeval_docs():
    start_at = 32
    parameters = OpenAICompletionParameters(
        max_tokens=3000,
    )
    processor = OpenAICompletionProcessor()
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/semeval_fa_da.json",
    )
    with source.open("r") as fin:
        jdocs = json.load(fin)
        for i, chunk in enumerate(chunks(jdocs, 10)):
            if i >= start_at:
                docs = [Document(**jdoc) for jdoc in chunk]
                for type, prompt in JINJA_PROMPTS.items():
                    parameters.prompt = prompt
                    parameters.completion_altText = type
                    docs = processor.process(docs, parameters)
                    # assert docs == HasLen(6)
                    sum_file = testdir / f"data/semeval_fa_da_{type}_{i}.json"
                    dl = DocumentList(__root__=docs)
                    with sum_file.open("w") as fout:
                        print(
                            dl.json(exclude_none=True, exclude_unset=True, indent=2),
                            file=fout,
                        )


@pytest.mark.skip(reason="Not a test")
@pytest.mark.parametrize("model", [m for m in CHAT_GPT_MODEL_ENUM])
def test_openai_prompt(model):
    parameters = OpenAICompletionParameters(
        model=model, max_tokens=120, completion_altText="completion"
    )
    processor = OpenAICompletionProcessor()
    docs_with_prompts = [
        (
            Document(
                identifier="1",
                text="séisme de magnitude 7,8 a frappé la Turquie",
                metadata={"language": "fr"},
            ),
            "Peux tu écrire un article de presse concernant: $text",
        ),
        (
            Document(
                identifier="2",
                text="j'habite dans une maison",
                metadata={"language": "fr"},
            ),
            "Peux tu me donner des phrases similaires à: $text",
        ),
        (
            Document(
                identifier="3",
                text="il est né le 21 janvier 2000",
                metadata={"language": "fr"},
            ),
            "Peux tu me donner des phrases similaires en changeant le format de date à: $text",
        ),
        (
            Document(
                identifier="4",
                text="""Un nuage de fumée juste après l’explosion, le 1er juin 2019.
                Une déflagration dans une importante usine d’explosifs du centre de la Russie a fait au moins 79 blessés samedi 1er juin.
                L’explosion a eu lieu dans l’usine Kristall à Dzerzhinsk, une ville située à environ 400 kilomètres à l’est de Moscou, dans la région de Nijni-Novgorod.
                « Il y a eu une explosion technique dans l’un des ateliers, suivie d’un incendie qui s’est propagé sur une centaine de mètres carrés », a expliqué un porte-parole des services d’urgence.
                Des images circulant sur les réseaux sociaux montraient un énorme nuage de fumée après l’explosion.
                Cinq bâtiments de l’usine et près de 180 bâtiments résidentiels ont été endommagés par l’explosion, selon les autorités municipales. Une enquête pour de potentielles violations des normes de sécurité a été ouverte.
                Fragments de shrapnel Les blessés ont été soignés après avoir été atteints par des fragments issus de l’explosion, a précisé une porte-parole des autorités sanitaires citée par Interfax.
                « Nous parlons de blessures par shrapnel d’une gravité moyenne et modérée », a-t-elle précisé.
                Selon des représentants de Kristall, cinq personnes travaillaient dans la zone où s’est produite l’explosion. Elles ont pu être évacuées en sécurité.
                Les pompiers locaux ont rapporté n’avoir aucune information sur des personnes qui se trouveraient encore dans l’usine.
                """,
                metadata={"language": "fr"},
            ),
            "Peux résumer dans un style journalistique le texte suivant: $text",
        ),
        (
            Document(
                identifier="5",
                text="Paris is the capital of France and Emmanuel Macron is the president of the French Republic.",
                metadata={"language": "en"},
            ),
            "Can you find the names of people, organizations and locations in the following text:\n\n $text",
        ),
    ]
    docs = []
    for doc, prompt in docs_with_prompts:
        parameters.prompt = prompt
        doc0 = processor.process([doc], parameters)[0]
        docs.append(doc0)
        assert doc0.altTexts == IsList(
            HasAttributes(name=parameters.completion_altText)
        )
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / f"en_{model.value}.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


@pytest.mark.skip(reason="Not a test")
def test_openai():
    parameters = OpenAICompletionParameters(
        system_prompt="Tu es un journaliste",
        max_tokens=120,
        best_of=3,
        n=3,
        completion_altText="completion",
    )
    processor = OpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Peux tu écrire un article de presse concernant: séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="Peux tu me donner des phrases similaires à: j'habite dans une maison",
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    for doc in docs:
        assert doc.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / "fr_default.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


# noqa: E501
@pytest.mark.skip(reason="Not a test")
@pytest.mark.parametrize("model", [m for m in CHAT_GPT_MODEL_ENUM])
def test_openai_text(model):
    parameters = OpenAICompletionParameters(
        model=model,
        system_prompt="Tu es un journaliste",
        max_tokens=120,
        best_of=3,
        n=3,
        completion_altText="completion",
    )
    processor = OpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Peux tu écrire un article de presse concernant: séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="Peux tu me donner des phrases similaires à: j'habite dans une maison",
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    for doc in docs:
        assert doc.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / f"fr_{model.value}.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


@pytest.mark.skip(reason="Not a test")
def test_runpod():
    parameters = OpenAICompletionParameters(
        base_url="https://u33htlbn4e1hwd-8000.proxy.runpod.net/v1",
        system_prompt="Tu es un journaliste",
        max_tokens=120,
        best_of=3,
        n=3,
        completion_altText="completion",
    )
    processor = OpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Peux tu écrire un article de presse concernant: séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="Peux tu me donner des phrases similaires à: j'habite dans une maison",
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    for doc in docs:
        assert doc.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / "fr_runpod.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


# noqa: E501
@pytest.mark.skip(reason="Not a test")
def test_q_and_a():
    prompt = """Répondre à la question en utilisant les segments suivants et en citant les références.
    Question: {{ doc.altTexts[0].text }}
    Segments: {{ doc.text }}"""

    parameters = OpenAICompletionParameters(
        max_tokens=2000,
        completion_altText=None,
        prompt=prompt,
    )
    processor = OpenAICompletionProcessor()
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/question_segments.json",
    )
    with source.open("r") as fin:
        jdoc = json.load(fin)
        docs = [Document(**jdoc)]
        docs = processor.process(docs, parameters)
        assert docs == HasLen(1)
        sum_file = testdir / "data/question_segments_answer.json"
        dl = DocumentList(__root__=docs)
        with sum_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
    # noqa: E501


@pytest.mark.skip(reason="Not a test")
def test_azure_endpoint():
    parameters = AzureOpenAICompletionParameters(
        system_prompt="Tu es un journaliste",
        max_tokens=1000,
        best_of=3,
        n=3,
        completion_altText="completion",
    )
    processor = AzureOpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Peux tu écrire un article de presse concernant: séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="Peux tu me donner des phrases similaires à: j'habite dans une maison",
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    for doc in docs:
        assert doc.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / "fr_azure_gpt_4.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))


@pytest.mark.skip(reason="Not a test")
def test_apollo_endpoint():
    parameters = ApolloOpenAICompletionParameters(
        system_prompt="Tu es un journaliste",
        max_tokens=1000,
        best_of=3,
        n=3,
        completion_altText="completion",
    )
    processor = ApolloOpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Peux tu écrire un article de presse concernant: séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="Peux tu me donner des phrases similaires à: j'habite dans une maison",
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    for doc in docs:
        assert doc.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / "fr_apollo_gpt_4.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))


@pytest.mark.skip(reason="Not a test")
def test_deepinfra_endpoint():
    parameters = DeepInfraOpenAICompletionParameters(
        model='mistralai/Mistral-Nemo-Instruct-2407',
        max_tokens=100,
        completion_altText="completion",
    )
    processor = DeepInfraOpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Peux tu écrire un article de presse concernant: séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="Peux tu me donner des phrases similaires à: j'habite dans une maison",
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    for doc in docs:
        assert doc.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / "fr_nemo.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))


@pytest.mark.skip(reason="Not a test")
def test_direct_deepinfra():
    PROMPT = """[INST]Answer the question in french using the given segments of a long document and making references of those segments ["SEGMENT"] with the segment number. 
Be short and precise as possible. If you don't know the answer, just say that you don't know. Don't try to make up an answer.
Question: Est-il prévu des congés rémunérés pour les femmes souffrant de douleurs menstruelles ?

SEGMENTS:
1. À l’heure où certaines entreprises ou même certaines collectivités prévoient des congés rémunérés pour les femmes souffrant de douleurs menstruelles importantes ou d’endométriose, une proposition de loi a été déposée au Sénat en ce sens le 18 avril 2023 par une sénatrice socialiste et plusieurs de ses collègues. Les femmes concernées pourraient faire l’objet d’un arrêt de travail ou encore télétravailler, sous certaines conditions. La proposition de loi prévoit aussi un congé payé pour les femmes (et leur conjoint) ayant subi une fausse couche.

2. La proposition de loi prévoit de créer un arrêt de travail indemnisé pour les femmes souffrant de dysménorrhée (règles douloureuses) ou d’endométriose (maladie gynécologique inflammatoire et chronique). Prescrit par un médecin ou une sage-femme, cet arrêt maladie autoriserait la salariée à interrompre son travail chaque fois qu’elle se trouverait dans l’incapacité physique de travailler, pour une durée ne pouvant excéder 2 jours par mois sur une période de 3 mois. Les IJSS, versées sans délai de carence, se calculeraient selon des règles dérogatoires favorables à la salariée.  Dans l’objectif d’éviter un arrêt de travail, la proposition de loi vise aussi à favoriser la possibilité de télétravail pour les femmes souffrant de règles douloureuses et invalidantes, via l'accord collectif ou la charte sur le télétravail lorsqu'il en existe un.    Enfin, le texte propose de créer sur justification, pour les femmes affectées par une interruption spontanée de grossesse, un congé rémunéré de 5 jours ouvrables. Le conjoint, concubin ou partenaire pacsé de la salariée aurait aussi droit à ce congé.    Reste à voir si cette 2e proposition de loi, déposée le 18 avril par une sénatrice socialiste et plusieurs de ses collègues, connaîtra un sort aussi favorable que la première.

3. Maternité, paternité, adoption, femmes enceintes dispensées de travail - L’employeur doit compléter une attestation de salaire lorsque le congé de maternité* débute (c. séc. soc. art. R. 331-5, renvoyant à c. séc. soc. art. R. 323-10).      Le même document est à compléter en cas de congé d’adoption*, de congé de paternité et d’accueil de l’enfant* ou, dans le cadre de la protection de la maternité, pour les femmes travaillant de nuit ou occupant des postes à risques dispensées de travail en raison d’une impossibilité de reclassement sur un poste de jour ou sans risques .      Il s’agit de la même attestation que celle prévue pour les arrêts maladie.

4. Grossesse pathologique liée au distilbène - Le distilbène (ou diéthylstilbestrol) prescrit il y a plusieurs années entraîne des grossesses pathologiques chez les femmes qui y ont été exposées in utero.      Les femmes chez lesquelles il est reconnu que la grossesse pathologique est liée à l’exposition in utero au distilbène bénéficient d’un congé de maternité à compter du premier jour de leur arrêt de travail (loi 2004-1370 du 20 décembre 2004, art. 32         ; décret 2006-773 du 30 juin 2006, JO 2 juillet).

5. Enfant né sans vie - L'indemnité journalière de maternité est allouée même si l'enfant n'est pas né vivant au terme de 22 semaines d'aménorrhée (c. séc. soc. art. R. 331-5). Pathologie liée au Distilbène - Bien que ce médicament ne soit plus prescrit, le Distilbène (ou diéthyltilbestrol) peut entraîner des grossesses pathologiques pour les femmes qui y ont été exposées in utero. Les femmes dont il est reconnu que la grossesse pathologique est liée à l’exposition in utero au Distilbène bénéficient d’un congé de maternité à compter du premier jour de leur arrêt de travail (loi 2004-1370 du 20 décembre 2004, art. 32, JO du 21). Ces femmes peuvent prétendre à l’IJSS de maternité dès le début de leur congé de maternité si elles remplissent les conditions d’ouverture du droit au congé légal de maternité (décret 2006-773 du 30 juin 2006, JO 2 juillet).

6. Possibilité de télétravailler pour les femmes souffrant de règles douloureuses Dans l’objectif d’éviter un arrêt de travail pour douleurs menstruelles, la proposition de loi vise à favoriser la possibilité de télétravail aux femmes souffrant de dysménorrhée (proposition de loi, art. 4).   À cet égard, l'accord collectif ou la charte sur le télétravail existant dans l’entreprise devrait préciser les modalités d’accès des salariées souffrant de règles douloureuses et invalidantes à une organisation en télétravail.    En toute logique, il ressort de l’exposé des motifs que cela ne viserait que les femmes dont l’activité professionnelle est compatible avec l’exercice du télétravail.      À noter : en dehors d’un accord ou d’une charte sur le télétravail, il est toujours possible à l’employeur et au salarié de convenir d’un recours au télétravail formalisé par tout moyen (c. trav. art. L. 1222-9).Une proposition de loi en faveur des femmes souffrant de douleurs menstruelles, d’endométriose, ou ayant subi une fausse couche
    [/INST]"""
    api_key = os.getenv("DEEPINFRA_OPENAI_API_KEY")
    deploy_infer_url = "https://api.deepinfra.com/v1/inference/meta-llama/Llama-2-70b-chat-hf"
    response = requests.post(deploy_infer_url, json={
        "input": PROMPT,
        "max_new_tokens": 4096,
        "temperature": 0.2
    },
                             headers={'Content-Type': "application/json",
                                      'Authorization': f"Bearer {api_key}"})
    if response.ok:
        result = response.json()
        texts = "\n".join([r['generated_text'] for r in result['results']])
        assert len(texts) > 0


# noqa: E501

@pytest.mark.skip(reason="Not a test")
def test_function_call_ner():
    candidate_labels = {
        'resource': 'RESOURCE',
        'organization': 'ORGANIZATION',
        'group': 'GROUP',
        'person': 'PERSON',
        'event': 'EVENT',
        'function': 'FUNCTION',
        'time': 'TIME'
    }
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/ner_long_prompt.txt",
    )
    with source.open("r") as fin:
        long_prompt = fin.read()

    parameters = OpenAICompletionParameters(
        model='gpt-4-turbo-preview',
        max_tokens=4096,
        temperature=0.2,
        prompt=long_prompt,
        function=OpenAIFunction.add_annotations,
        candidate_labels=candidate_labels
    )
    processor = OpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Selon l'agence de presse semi-officielle ISNA, les utilisateurs de carburant auraient reçu un message indiquant « cyberattaque 64411 », un numéro d'urgence lié au bureau du guide suprême iranien, l'ayatollah Ali Khamenei.",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="""En   Birmanie,   un   chauffeur   de   l'OMS,   l'Organisation   mondiale   de   la   santé,   qui   transportait   des 
échantillons de tests au coronavirus, a été tué dans une attaque dans l'État rakhine, une région en 
proie à des violences entre groupes rebelles et militaires.""",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="3",
            text="""Un fonctionnaire du ministère de la Santé et des Sports, présent 
dans le véhicule, a été blessé.""",
            metadata={"language": "fr"},
        ),
    ]

    results = processor.process(deepcopy(docs), parameters)
    assert results == HasLen(3)
    doc0 = results[0]
    for a in doc0.annotations:
        assert a.text == doc0.text[a.start:a.end]
    result_file = source.with_suffix(".json")
    dl = DocumentList(__root__=results)
    with result_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))

    source = Path(
        testdir,
        "data/ner_json_prompt.txt",
    )
    with source.open("r") as fin:
        json_prompt = fin.read()

    parameters.prompt = json_prompt
    parameters.function = None
    parameters.completion_altText = "json"
    results = processor.process(deepcopy(docs), parameters)
    assert results == HasLen(3)
    doc0 = results[0]
    result_file = source.with_suffix(".json")
    dl = DocumentList(__root__=results)
    with result_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))

    source = Path(
        testdir,
        "data/ner_xml_prompt.txt",
    )
    with source.open("r") as fin:
        xml_prompt = fin.read()
    parameters.prompt = xml_prompt
    parameters.function = None
    parameters.completion_altText = "xml"
    results = processor.process(deepcopy(docs), parameters)
    assert results == HasLen(3)
    doc0 = results[0]
    result_file = source.with_suffix(".json")
    dl = DocumentList(__root__=results)
    with result_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))


@pytest.mark.skip(reason="Not a test")
def test_function_call_ner_dbrx():
    candidate_labels = {
        'resource': 'RESOURCE',
        'organization': 'ORGANIZATION',
        'group': 'GROUP',
        'person': 'PERSON',
        'event': 'EVENT',
        'function': 'FUNCTION',
        'time': 'TIME'
    }
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/ner_long_prompt.txt",
    )
    with source.open("r") as fin:
        long_prompt = fin.read()

    parameters = DeepInfraOpenAICompletionParameters(
        model='databricks/dbrx-instruct',
        max_tokens=4096,
        temperature=0.2,
        prompt=long_prompt,
        completion_altText="llm",
        function=OpenAIFunction.add_annotations,
        candidate_labels=candidate_labels
    )
    processor = DeepInfraOpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Selon l'agence de presse semi-officielle ISNA, les utilisateurs de carburant auraient reçu un message indiquant « cyberattaque 64411 », un numéro d'urgence lié au bureau du guide suprême iranien, l'ayatollah Ali Khamenei.",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="""En   Birmanie,   un   chauffeur   de   l'OMS,   l'Organisation   mondiale   de   la   santé,   qui   transportait   des 
échantillons de tests au coronavirus, a été tué dans une attaque dans l'État rakhine, une région en 
proie à des violences entre groupes rebelles et militaires.""",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="3",
            text="""Un fonctionnaire du ministère de la Santé et des Sports, présent 
dans le véhicule, a été blessé.""",
            metadata={"language": "fr"},
        ),
    ]

    results = processor.process(deepcopy(docs), parameters)
    assert results == HasLen(3)
    doc0 = results[0]
    for a in doc0.annotations:
        assert a.text == doc0.text[a.start:a.end]
    result_file = source.with_suffix(".json")
    dl = DocumentList(__root__=results)
    with result_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))

    source = Path(
        testdir,
        "data/ner_json_prompt.txt",
    )
    with source.open("r") as fin:
        json_prompt = fin.read()

    parameters.prompt = json_prompt
    parameters.function = None
    parameters.completion_altText = "json"
    results = processor.process(deepcopy(docs), parameters)
    assert results == HasLen(3)
    doc0 = results[0]
    result_file = source.with_suffix(".json")
    dl = DocumentList(__root__=results)
    with result_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))

    source = Path(
        testdir,
        "data/ner_xml_prompt.txt",
    )
    with source.open("r") as fin:
        xml_prompt = fin.read()
    parameters.prompt = xml_prompt
    parameters.function = None
    parameters.completion_altText = "xml"
    results = processor.process(deepcopy(docs), parameters)
    assert results == HasLen(3)
    doc0 = results[0]
    result_file = source.with_suffix(".json")
    dl = DocumentList(__root__=results)
    with result_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))


@pytest.fixture
def expected_en():
    return {
        "Sport": "The french team is going to win Euro 2021 football tournament",
        "Politics": "Who are you voting for in 2021?",
        "Science": "Coronavirus vaccine research are progressing",
    }


@pytest.mark.skip(reason="Not a test")
def test_function_call_cat(expected_en):
    candidate_labels = {
        'sport': 'Sport',
        'politics': 'Politics',
        'science': 'Science',
    }

    EXCL_CLAUSE = "\nThe task is exclusive, so only choose one label from what I provided and write it as a single line.\n"
    NO_EXCL_CLAUSE = "\nThe task is not exclusive, so if more than one label is possible, please just write one label per line.\n"

    excl_prompt = """You are an expert Text Classification system. Your task is to accept Text as input and provide a category for the text based on the predefined labels.
{%- set labels=[] -%}
{%- for l in parameters.candidate_labels.values() -%}
  {%- do labels.append('"' + l + '"') -%}
{%- endfor %}
Classify the text below to one of the following labels: {{ labels|join(', ') }}
The task is exclusive, so only choose one label from what I provided and write it as a single line.""" + EXCL_CLAUSE + """Text: {{doc.text}}
Result:
"""
    no_excl_prompt = """You are an expert Text Classification system. Your task is to accept Text as input and provide a category for the text based on the predefined labels.
    {%- set labels=[] -%}
    {%- for l in parameters.candidate_labels.values() -%}
      {%- do labels.append('"' + l + '"') -%}
    {%- endfor %}
    Classify the text below to one of the following labels: {{ labels|join(', ') }}
    The task is exclusive, so only choose one label from what I provided and write it as a single line.""" + NO_EXCL_CLAUSE + """Text: {{doc.text}}
    Result:
    """
    parameters = OpenAICompletionParameters(
        model=OpenAIModel.gpt_3_5_turbo,
        completion_altText=None,
        prompt=excl_prompt,
        function=OpenAIFunction.add_categories,
        candidate_labels=candidate_labels
    )
    processor = OpenAICompletionProcessor()
    docs = [Document(text=t) for t in expected_en.values()]
    docs = processor.process(docs, parameters)
    for expected_label, doc in zip(expected_en.keys(), docs):
        assert doc.categories[0].label == expected_label

    parameters.prompt = no_excl_prompt
    docs = [Document(text=t) for t in expected_en.values()]
    docs = processor.process(docs, parameters)
    for expected_label, doc in zip(expected_en.keys(), docs):
        assert doc.categories[0].label == expected_label


@pytest.mark.skip(reason="Not a test")
def test_cairninfo():
    prompt = """Vous disposez d'un article de revue scientifique couvrant un sujet dans le domaine des sciences humaines et sociales ou des sciences dures.  L'article peut faire une ou plusieurs pages.
Vous devez écrire un long résumé en français d'une longueur de 600 mots minimum.
Le résumé doit expliquer les points clés de l'article. 
Utilisez un vocabulaire précis et varié.
Évitez les répétitions.
Le résumé doit être complet et transmettre toutes les idées développées dans l'article.
Texte : $text
"""

    parameters = DeepInfraOpenAICompletionParameters(
        model="cognitivecomputations/dolphin-2.6-mixtral-8x7b",
        max_tokens=6000,
        completion_altText="résumé",
        prompt=prompt,
    )
    processor = DeepInfraOpenAICompletionProcessor()
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/cairninfo.json",
    )
    with source.open("r") as fin:
        jdoc = json.load(fin)
        doc = Document(**jdoc)
        docs = processor.process([doc], parameters)
        assert docs == HasLen(1)
        sum_file = testdir / "data/cairninfo_summary.json"
        dl = DocumentList(__root__=docs)
        with sum_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
    # noqa: E501


@pytest.mark.skip(reason="Not a test")
def test_resume_mixtral():
    text = """Jérusalem, ville sainte contestée
La situation ecclésiale diverse et complexe
Matthias Vogt

Jérusalem, ville sainte de trois religions, lieu de la passion, de la mort et de la résurrection de Jésus Christ, berceau du christianisme, destination de pèlerinages de millions de chrétiens du monde entier, lieu de rêves pour beaucoup qui, pour des raisons sociales ou politiques ne peuvent s’y rendre dont les chrétientés de la majorité de pays arabes et de beaucoup de pays qui se disent musulmans. Jérusalem, centre de la communauté chrétienne naissante dont témoignent les Actes des Apôtres, « Église-mère » de toutes les Églises, comme aiment à le répéter les clercs de la ville sainte, noyau de l’œcuménisme mais aussi point chaud de conflits interconfessionnels et foyer d’une communauté chrétienne multiforme. C’est sur la situation des Églises de Jérusalem et des chrétiens de la ville que nous voulons mettre l’accent dans cet article.
Situation actuelle de Jérusalem
De nos jours, Jérusalem est une ville d’environ 966 000 habitants dont la majorité sont juifs (567 000 ou 59 %) et environ 366 000 musulmans (38 %). Selon les données de l’année 2021 publiées par le Bureau israélien des statistiques, il y a à Jérusalem, Est et Ouest confondus, 12 900 chrétiens (1,3 % de la population totale), dont 9800 chrétiens arabes (ou 2,6 % de la population arabe). En 1944, les chrétiens comptent 19 % de la population (29 400 chrétiens parmi 30 600 musulmans et 97 000 juifs) ou quasiment la moitié de la population non-juive de la ville. Il faut donc constater une chute dramatique de la quote-part chrétienne. Ce qui pèse lourd chez les chrétiens de Jérusalem, c’est que cette ville considérée comme un « espace chrétien » n’existe plus, en tant que telle, depuis 1948 malgré la multitude d’églises, de lieux saints et d’institutions chrétiennes.
Pour les Juifs, Jérusalem est considérée la ville la plus conservatrice du pays. Avec son grand nombre d’écoles religieuses (yeshiva, pl. yeshivot), surtout dans le quartier juif de la vieille ville, le nombre croissant de quartiers ultra-orthodoxes à Jérusalem-Ouest et la présence de groupes nationalistes juifs à l’intérieur des murailles médiévales, l’ambiance dans la ville est de plus en plus hostile aux populations chrétienne et musulmane. Les implantations des colons nationalistes et religieux dans les quartiers chrétiens et musulmans de la vieille ville et dans les quartiers résidentiels arabes de Jérusalem-Est (surtout Sheikh Jarrah, Abu Tor et Silwan) constituent une provocation envers les habitants palestiniens et sont les lieux de multiples conflits violents entre colons, Palestiniens et forces de l’ordre israéliennes.
Pour les musulmans, Jérusalem se trouve au centre des préoccupations palestiniennes mais aussi mondiales vu l’importance des sanctuaires islamiques sur le Haram al-Sharîf. Deux mouvements islamiques extrémistes sont présents dans la ville : le Hamas (Mouvement de résistance islamique), né de la Société des Frères musulmans, et le Hizb al-tahrîr (Parti de la libération), mouvement islamique international, né en Palestine, qui vise à imposer l’application stricte de la loi islamique (sharî’a) et à établir un état islamique de type califal. Les deux mouvements se montrent peu favorables aux non-musulmans auxquels ils assignent, dans leur projet de cité, une place régie par les lois islamiques, c’est-à-dire un statut inférieur à celui des musulmans. Les manifestations des adhérents à ces deux mouvements, surtout aux alentours de la mosquée al-Aqsa, créent une ambiance peu rassurante pour les chrétiens de Jérusalem et remettent en question, de plus en plus, l’unité entre chrétiens et musulmans à cause du mouvement national palestinien.
Les Palestiniens de Jérusalem, chrétiens et musulmans, participent peu à la vie politique de la ville : dans les élections municipales les suffrages arabes sont bas, la participation à la chose publique étant considérée comme contribution à la « normalisation » d’une situation irrégulière. Ce n’est donc pas seulement à cause de la majorité absolue des habitants juifs de Jérusalem que la municipalité est dominée par la composante juive. Pour la politique israélienne, aussi bien sur le plan national que municipal, il n’y a aucun doute que Jérusalem est la « capitale éternelle et indivisible » de l’État juif telle que déclarée, en 1980, par la Knesset, le parlement israélien.
Les projets d’aménagement et de développement pris en charge par la municipalité de Jérusalem, sont considérés par la population arabe comme des tentatives plus ou moins dissimulées d’appropriation de terrains qui se trouvent encore entre les mains de propriétaires palestiniens. Des parcelles appartenant aux Églises ainsi qu’à des congrégations religieuses sont aussi menacées. Le projet d’aménagement d’un parc national sur les terrains pentus du Mont des Oliviers qui appartiennent à des Églises suscite l’inquiétude des chefs d’Églises. De même, l’acquisition par les associations de colons juifs d’immeubles, dans le quartier chrétien de la vieille ville, a suscité la critique des représentants des Églises. Même si certaines de ces transactions immobilières sont légales, les prix offerts, souvent le double du prix du marché, laissent apparaître un manque de droiture morale. La non-ingérence des autorités israéliennes compétentes trahit l’absence de volonté de protéger l’équilibre traditionnel et fragile des communautés religieuses dans la ville sainte.
La situation ecclésiale et œcuménique
Les chrétiens de Jérusalem se répartissent sur 13 communautés reconnues ; du côté orthodoxe : grecque, arménienne, syriaque, copte et éthiopienne ; du côté catholique : latine (catholique romaine), grec-melkite, arménienne, syriaque, maronite et chaldéenne ; du côté des Églises issues de la Réforme : épiscopale (anglicane) et luthérienne, sans compter différentes communautés protestantes et pentecôtistes non reconnues. Ces Églises comptent un nombre inégal de croyants de langue arabe vivant à Jérusalem : les catholiques de rite latin sont environ 5400 (55 %), les grecs orthodoxes 2300 (23 %), les melkites 860 (9 %), les arméniens orthodoxes 500 (5 %), les syriens orthodoxes 400 (4 %) et les autres 330 (3 %).
L’Église grecque-orthodoxe est dirigée par le patriarche de Jérusalem, assisté dans l’exercice de ses fonctions par 14 évêques titulaires. Ils sont tous membres de la Confrérie du Saint-Sépulcre (Confrérie des hagiotaphites) dont la mission est de préserver les propriétés de l’Église orthodoxe dans les lieux saints et de préserver le caractère hellénique du patriarcat. La communauté arabe est représentée dans la Confrérie par un seul évêque d’origine palestinienne ou jordanienne. Le fait que le clergé supérieur soit presque exclusivement grec, alors que les prêtres et les fidèles sont arabes, provoque régulièrement des tensions et des reproches de la part du laïcat selon lesquels la hiérarchie ne défend pas avec suffisamment de vigueur les intérêts de la communauté face à l’État israélien. Les activités sociales et humanitaires sont principalement menées par des associations de laïcs. Depuis les années 1990, les croyants arabes sont préoccupés par l’immigration en provenance des pays de l’ex-Union soviétique qui a entraîné une nette augmentation de communautés orthodoxes de langue non arabe. Ces fidèles vivent entièrement dans le milieu juif israélien et n’ont aucun contact avec les communautés arabes. Par leur présence, le caractère jusqu’alors presque exclusivement arabe de la communauté grecque-orthodoxe de Jérusalem et de Terre Sainte s’est affaibli. Cela ne renforce pas les prétentions des laïcs arabes d’avoir leur mot à dire dans la gestion des biens et leur demande d’arabisation du patriarcat.
L’Église romaine catholique (latine) est représentée par le patriarche latin de Jérusalem. Créé en 1099 pendant les croisades, le patriarcat latin a été rétabli en 1847. L’Église latine compte un grand nombre d’ordres et de congrégations (102 en 2018), souvent d’origine française et italienne. Elle gère de nombreuses institutions éducatives et sociales. Le patriarche de l’Église grecque melkite catholique se fait représenter à Jérusalem par un évêque avec le titre de protosyncelle, ayant juridiction sur la ville sainte et les territoires palestiniens. Les syriens catholiques et les arméniens catholiques ont tous les deux un exarque siégeant à Jérusalem. Les maronites vivent surtout dans le Nord d’Israël et c’est donc à Haïfa que réside leur évêque.
Les arméniens orthodoxes sont représentés à Jérusalem par un patriarche et un nombre de croyants inférieur à 1500. Ils se composent de trois éléments : les « anciens » arméniens de Terre Sainte, les descendants des réfugiés arméniens survivants du Génocide lors de la Première Guerre mondiale, et les immigrés arméniens venus après la chute de l’Union soviétique. Les arméniens vivent surtout dans leur quartier de la vieille ville et à Jérusalem-Ouest. Ils entretiennent des contacts avec la population palestinienne ou juive selon leurs préférences et leur lieu d’habitation. La plupart des arméniens venus avant 1948 se sentent solidaires des aspirations palestiniennes. L’organisation du patriarcat arménien repose avant tout sur la Confrérie de Saint Jacques et sur un conseil composé de dignitaires religieux appartenant à l’intérieur et à l’extérieur de la Terre Sainte.
Les syriaques et les coptes orthodoxes ont chacun un métropolite à Jérusalem. Depuis le milieu du XIXe siècle, l’Église copte se dispute avec l’Église éthiopienne la propriété du monastère de Deir al-Sultan située près du Saint-Sépulcre. La communauté éthiopienne a longtemps été composée d’un petit nombre de familles qui se retiraient dans les lieux saints afin de mener une vie de prière. En raison des bonnes relations politiques entre Israël et l’Éthiopie, un nombre important de travailleurs immigrés viennent en Israël et, depuis quelques années, de plus en plus de réfugiés. Les Éthiopiens vivent autour des monastères éthiopiens de Jérusalem-Ouest et de la vieille ville où ils se mêlent aussi bien avec les Juifs qu’avec les Arabes. Ils constituent ainsi une particularité parmi les chrétiens orientaux de Terre Sainte.
L’origine des évêchés épiscopal et luthérien remonte à un évêché commun anglican-luthérien, créé en 1841 par un accord entre la Grande-Bretagne et la Prusse. Cette dernière décidant de quitter l’union des Églises en 1886, l’Église anglicane en garde seule l’évêché. Aujourd’hui, la compétence de l’archevêque épiscopal de Jérusalem couvre la Palestine, Israël, la Jordanie, le Liban et la Syrie. La communauté luthérienne allemande a suivi sa propre voie, indépendamment de l’évêché anglican de Jérusalem, ses activités étant soutenues par le Jerusalemverein (Association de Jérusalem), créé à Berlin en 1853. Jusqu’à la Première Guerre mondiale, l’empereur Guillaume II a soutenu l’association et s’est lui-même rendu en Terre Sainte en 1898. À cette occasion, il a inauguré l’église protestante allemande du Rédempteur dans la vieille ville de Jérusalem. À la suite de ce voyage, est créée la fondation de l’impératrice Auguste Victoria, sur le Mont des Oliviers. La communauté évangélique arabe est issue, pour une part importante, de sortants de « l’Orphelinat syrien » de la famille Schneller. En 1929, naît la communauté évangélique palestinienne de Jérusalem, restée pourtant étroitement liée à la communauté luthérienne allemande. En 1958, se constitue l’Église luthérienne sous le nom d’Église évangélique luthérienne de Jordanie (Evangelical-Lutheran Church of Jordan, ELCJ) qui sera dirigée dès 1979 par un évêque dont le siège sera à Jérusalem.
La situation œcuménique à Jérusalem est considérée comme l’une des pires au monde. Des conflits sur les privilèges des Églises quant aux lieux saints ralentissent le rapprochement œcuménique. Un facteur extérieur rapproche pourtant les Églises de Terre Sainte l’une de l’autre depuis les années 1980 : la menace de « l’israélisation » de la ville sainte qui a forcé les chefs d’Églises de se montrer unis. Depuis de longues années, ont-ils pris l’habitude de publier des déclarations communes.
L’Assemblée des ordinaires catholiques de Terre Sainte a promulgué, en 2021, des directives œcuméniques. Elles visent surtout la participation des fidèles à la vie sacramentelle et prennent en considération la situation interconfessionnelle de beaucoup de familles chrétiennes. Sur le plan spirituel, on célèbre, à la fin janvier de chaque année, la semaine de l’unité des chrétiens par des prières communes, offertes à tour de rôle dans les églises de toutes les communautés chrétiennes. La situation exceptionnelle de la pandémie COVID-19 en mars 2020, a même donné l’occasion de dire une prière interreligieuse pour le salut de tous. Y ont participé les représentants de plusieurs Églises, les grands rabbins ashkénaze et séfarade, ainsi que des représentants de l’islam et des Druzes.
Jérusalem – Destination des pèlerins du monde entier
Le patriarcat grec-orthodoxe s’occupe de l’accueil des pèlerins orthodoxes. Reste à souligner la position particulière de l’Église russe-orthodoxe qui gère à Jérusalem plusieurs églises, monastères et hospices pour pèlerins (le fameux Russian Compound près de la Jaffa Street à Jérusalem-Ouest et l’église russe au pied du Mont des Oliviers), établis depuis la fin du XIXe siècle par la Société impériale orthodoxe de Palestine (fondée en 1882, confirmée et réformée la dernière fois en 2003). La société défend en Terre Sainte les intérêts du patriarcat de Moscou et s’occupe des pèlerins russes.
Côté catholique, la majorité des lieux saints sont gardés par les Franciscains de la Custodie (établie par le pape Clément VI en 1342). Avec l’aide de frères de différents pays, la Custodie dirige une bonne partie de la pastorale de pèlerins catholiques qui pratiquent diverses langues. À souligner aussi l’engagement social très important de la Custodie envers les chrétiens de Jérusalem, surtout dans le secteur de l’habitation et des bourses d’études.
Les pèlerins des pays arabes se sont faits rares depuis l’occupation de Jérusalem-Est par Israël en 1967. Le pape copte-orthodoxe Chenouda III (1971-2012) a interdit à ses fidèles le pèlerinage à Jérusalem au moment où l’Égypte et Israël concluaient un traité de paix en 1979. Le pape Tawadros (2012-), après s’être lui-même rendu à Jérusalem en 2015 à l’occasion des obsèques du métropolite copte, a levé cette interdiction en janvier 2022. Suite à cette mesure, 5000 Égyptiens approximativement se sont rendus à Jérusalem pour les célébrations pascales de 2022. Les chrétiens palestiniens se félicitent de cette présence de coreligionnaires arabes et la considèrent comme un renforcement important de leur position dans la ville sainte. Les pèlerins jordaniens, de leur part, sont peu nombreux. Ils peuvent demander des visas de groupe pour visiter les lieux saints à Jérusalem, en Israël et dans les territoires palestiniens, mais très peu en font usage. Aux fidèles du Liban et de la Syrie, la visite des lieux saints reste interdite, l’état de guerre qui règne toujours entre leurs pays et l’État d’Israël interdit toute communication avec l’État juif et ceci malgré la visite pastorale du patriarche Béchara Raï auprès de la communauté maronite d’Israël en 2014.
Le service religieux, l’entretien des églises, la préservation des droits de propriété et l’assistance aux pèlerins constitue une part importante du caractère des Églises de Jérusalem. Les droits de propriété et les privilèges sont régis par le « statu quo » de 1757, modifié en 1852. Cette réglementation n’a pas été modifiée, notamment parce que les Églises veillent jalousement sur leurs droits et privilèges. Ainsi les Églises grecque-orthodoxe, catholique, arménienne, copte, syriaque et éthiopienne jouissent-elles de droits sur des parties spécifiques de l’église du Saint-Sépulcre. En revanche, la clé se trouve depuis des siècles entre les mains de deux familles musulmanes. Les grecs, les arméniens, les coptes et les syriaques se partagent la propriété de l’église de la Nativité à Bethléem. Les catholiques n’ont qu’un droit d’accès à la grotte de la Nativité située sous la basilique. Mais ils ont leur propre église, directement rattachée à l’église byzantine. Les conflits interconfessionnels ont nettement diminué depuis que les travaux de restauration et de conservation, exécutés en entente cordiale par les différentes Églises dans l’édicule du Saint-Sépulcre (2016-2017), la basilique de la Nativité (2013-2020) et sous les pavées de la rotonde du Saint-Sépulcre (2022-), ce qui a renforcé le sentiment de confiance et de solidarité.
La vie sociale et politique des chrétiens de Jérusalem
Statut légal
Les chrétiens arabes de Jérusalem, comme tous les Palestiniens de la partie orientale de la ville, peuvent avoir un passeport jordanien. De plus, 52 % des chrétiens palestiniens de la ville sont titulaires d’une carte d’identité israélienne leur permettant la résidence permanente à Jérusalem, statut spécial accordé aux Palestiniens de Jérusalem après l’occupation israélienne de la ville en 1967. Depuis 2005, 44 % des chrétiens ont obtenu, en plus de cela, la citoyenneté israélienne (en 2005, seulement 5 % l’avaient). Ils hésitent donc entre leurs espoirs d’une future autonomie palestinienne dans Jérusalem-Est et les avantages que leur offre l’État juif. La citoyenneté israélienne leur offre l’accès au régime d’assurance nationale, au système de soins de santé, aux allocations de chômage et d’invalidité et aux prestations de retraite. Le choix de la citoyenneté israélienne n’est donc pas nécessairement lié à un changement d’opinion politique.
Les options de mariage des chrétiens de Jérusalem sont limitées par la loi israélienne, dite de « regroupement familial », promulguée en 2003. Cette loi empêche les familles non-juives d’obtenir des droits de résidence et d’entrée à Jérusalem. Elle porte également préjudice aux enfants nés dans les territoires palestiniens de parents résidant à Jérusalem-Est. Environ 300 familles chrétiennes de Jérusalem ont souffert de cette loi, en particulier les couples mariés après mai 2002. Il faut savoir que 16 % des familles chrétiennes de Jérusalem ont un parent originaire de Cisjordanie, principalement de Bethléem et de Ramallah. La loi restreint, de plus, les possibilités des chrétiens de Jérusalem de conclure des mariages avec un partenaire de la Cisjordanie. Étant donné les relations étroites entre familles chrétiennes hiérosolymitaines et bethléemites, cela est ressenti comme très douloureux et constitue une raison importante pour l’émigration des chrétiens. De nombreuses organisations internationales, israéliennes et palestiniennes, de défense des droits de l’homme ont fait pression contre cette loi, y compris la Société de Saint Yves (organisation de défense des droits de la personne sous les auspices du Patriarcat latin de Jérusalem) [12][12]Akroush, Jerusalem Christian Youth, 2019, p. 16..
La famille chrétienne
Depuis 2012, on constate une baisse du nombre de mariages chrétiens. Entre 2012 et 2019, on compte en moyenne chaque année 25 à 30 nouveaux mariages. L’âge médian des mariés chrétiens est de 29,2 ans pour les hommes et de 25,6 ans pour les femmes (données de 2016). 37 % de familles chrétiennes ont trois enfants, 31 % en ont quatre et 17 % deux. En comparant le taux de fécondité, les chrétiens ont le taux de fécondité le plus bas. Par conséquent, la communauté chrétienne de Jérusalem est, en moyenne, nettement plus âgée que la communauté musulmane (38 % des musulmans ont moins de 15 ans par rapport à 21 % des chrétiens). Quant aux personnes âgées (65 ans et plus), elles représentent 4 % de la population musulmane contre 14 % de la population chrétienne. L’âge médian dans la communauté chrétienne est de 34 ans, contre 21 ans dans la communauté musulmane.
La plupart des familles chrétiennes se présentent comme appartenant à la classe moyenne (90 %). Ceux qui s’identifient comme pauvres s’élèvent à 7 %. Dans plus de la moitié des familles chrétiennes (55 %), les deux parents travaillent, tandis que 44 % des familles n’ont qu’un seul soutien de famille, le plus souvent, c’est le père.
Les chrétiens arabes de Jérusalem vivent surtout en trois zones : au centre (vieille ville, Ras al-Amoud, Beit Faji), au Nord (Kufur Aqab, Anata, Beit Hanina, Shufat) et au Sud (Beit Safafa, Sharafat, Tantur). De plus en plus de familles chrétiennes achètent des propriétés dans les quartiers juifs, comme à Pisgat Ze’ev, ou acceptent de loger dans de nouveaux quartiers périphériques comme Talpiot-Est et Gilo. 30 % des familles chrétiennes sont propriétaires de leur appartement, 48 % vivent dans des appartements loués, tandis que 22 % habitent dans des propriétés « protégées » d’Église. Ces chiffres sont inquiétants si l’on considère que le taux d’accès à la propriété en Israël est de 66,5 %. Les coûts de loyer peuvent atteindre jusqu’à 40 % du revenu mensuel d’une famille, ce qui en fait la plus grande charge financière. Si l’on tient compte de tous les facteurs, on peut affirmer que plus de 60 % des familles chrétiennes sont menacées et vivent sous le seuil de la pauvreté. Elles peuvent à peine finir le mois sans dettes ou sans aide sociale de la part des Églises et des organisations caritatives.
Ainsi, près de 500 familles chrétiennes de Jérusalem reçoivent une aide financière sous diverses formes au moins une fois par an. Un quart des jeunes chrétiens reçoivent une aide financière de leurs Églises soit dans le cadre d’un programme d’aide sociale, soit sous la forme d’une aide aux études fournie par les Églises ou les écoles. La Custodie de Terre Sainte est le principal fournisseur de bourses d’études, offrant environ 40 bourses chaque année. Le patriarcat grec-orthodoxe offre plusieurs bourses d’études par an par le biais de l’école Saint Dimitri, mais pas nécessairement à des chrétiens. La Société de Saint-Vincent de Paul offre une dizaine de bourses d’études pour la formation professionnelle ou l’accueil de chrétiens pauvres. Le Secrétariat de solidarité, institution de l’Église catholique, offre des aides pour les frais de scolarité à plus de 2000 élèves chrétiens à Jérusalem, en Palestine, en Israël et en Jordanie.
Les écoles chrétiennes
La grande majorité des étudiants chrétiens de Jérusalem (98 %) sont inscrits dans des écoles chrétiennes. Cependant, on observe une tendance croissante parmi les Palestiniens – y compris les chrétiens – à s’inscrire dans les écoles gouvernementales israéliennes afin d’être mieux préparés au marché du travail israélien.
Les Églises et les organisations qui leur sont liées gèrent douze écoles à Jérusalem qui accueillent 1660 élèves chrétiens et plus de 5500 élèves musulmans. Huit de ces douze écoles sont situées dans et autour de la vieille ville. Les écoles chrétiennes sont le seul endroit où musulmans et chrétiens passent du temps ensemble, où ils peuvent faire connaissance au-delà de rencontres courtes et banales de tous les jours. Les écoles chrétiennes ont donc la responsabilité de promouvoir la coexistence, l’acceptation de l’autre et la démocratie, et d’enseigner l’histoire de la Terre Sainte dans une perspective chrétienne (y compris la période byzantine), ce qui ne fait partie ni du curriculum des écoles publiques israéliennes ni palestiniennes.
Par rapport aux autres écoles privées, municipales et islamiques (awqâf), les écoles chrétiennes jouissent d’une excellente réputation en termes de qualité de l’enseignement et en vue des certifications proposées, tant sur le plan local qu’international. Toutes les écoles chrétiennes suivent le programme palestinien, au moins jusqu’à la sixième année, avant de décider de s’engager ou dans le Tawjihi palestinien ou dans d’autres programmes tels que le General certificate of education (GCE) britannique, l’Abitur allemand (Schmidt’s Girls College), ou le Bagrut israélien. Les manuels palestiniens utilisés sont pourtant très déficitaires quant à la présentation des religions autres que l’islam et des périodes historiques anté-islamiques de la Palestine. Un rapport inédit du Centre œcuménique de théologie de la libération – Sabeel déplore que le curriculum palestinien qualifie chrétiens et juifs d’infidèles, qu’il préconise un califat islamique et qu’il insiste sur le port du hijab ou robe islamique. Un autre problème du système scolaire à Jérusalem-Est, y compris pour les écoles chrétiennes : à la fin de leurs études scolaires, à peine un tiers de chrétiens peuvent communiquer en hébreu alors que cette langue est la seule langue officielle dans les bureaux gouvernementaux et municipaux qui contrôlent tous les aspects de la vie à Jérusalem et en Israël.
En plus de leur rôle éducatif essentiel, les écoles chrétiennes sont sans doute les meilleurs forums pour la coexistence et la paix civile entre musulmans et chrétiens. Les musulmans qui étudient dans les écoles chrétiennes sont considérés comme les véritables agents de changement aux côtés de leurs concitoyens chrétiens. Les écoles chrétiennes s’investissent ainsi dans le développement d’êtres humains moralement responsables, et forment les meilleurs leaders de la société, démocratiques, énergiques et d’esprit ouvert quelle que soit leur croyance. Grâce à leur plus grande ouverture sur le monde vu le caractère international des congrégations religieuses ou institutions qui les soutiennent, les écoles chrétiennes de Jérusalem jouissent d’une plus grande liberté d’enseignement et vont au-delà des seuls textes éducatifs pour proposer à leurs étudiants des modèles de citoyenneté et des pratiques sociales et politiques qui favorisent la coexistence et la solidarité intercommunautaires.
Les Églises et leurs services
Malgré le nombre modeste de fidèles, les Églises en tant qu’institutions sont très fortes, grâce à la solidarité de l’Église universelle. Cela concerne les secteurs d’éducation, santé, culture, protection sociale et développement. Sur le plan culturel, il faut mentionner les nombreux centres communautaires, les clubs et les scouts, tous les trois régulièrement organisés selon les appartenances confessionnelles. Le secteur de la santé aussi joue un rôle important dans l’engagement des Églises qui gèrent cinq hôpitaux dans la ville sainte dont le plus grand est l’hôpital Auguste Victoria, géré par la Fédération luthérienne mondiale. Ces institutions emploient un total de 1200 salariés et accueillent plus de 330 000 patients par année, toute appartenance religieuse confondue.
Quant au secteur de la protection sociale, il concerne l’accueil et la réhabilitation de personnes handicapées, l’aide sociale, l’accueil de personnes âgées et la défense des droits de l’homme. À mentionner en particulier la Greek Orthodox Benevolent Society, le Good Samaritan Eldery Center situé dans un immeuble de la vieille ville appartenant au patriarcat grec-orthodoxe mais à vocation œcuménique, le foyer de personnes âgées des Sœurs de Notre Dame des Douleurs à Jérusalem-Est, les activités sociales de la Société de Saint Vincent de Paul, de Caritas Jérusalem et finalement la Société de Saint Yves pour la défense des droits de la personne (patriarcat latin de Jérusalem). Finalement, il faut mentionner les organisations internationales de développement à vocation chrétienne qui ont des branches ou bureaux à Jérusalem. Je ne peux conclure ce chapitre sans faire mention du Christian Information Center, tenu par la Custodie de Terre Sainte des Franciscains. Le centre s’occupe de la production médiatique, la distribution d’informations et de nouvelles sur tout ce qui concerne la vie chrétienne à Jérusalem, en Palestine et en Israël.
La vie des chrétiens en Israël et Palestine
Israël
L’image des chrétiens de Jérusalem serait incomplète sans un regard sur les chrétiens dans les territoires palestiniens et en Israël. Environ 127 000 chrétiens palestiniens vivent dans l’État d’Israël (sans Jérusalem-Est). La majorité d’entre eux vivent en Galilée, à Haïfa et dans les villes de Jaffa, Ramla et al-Ludd. Ils appartiennent majoritairement aux Églises grecques-melkites catholiques, grecques-orthodoxes et latines. Dans le Nord, il y a également quelques maronites. Ils jouissent de la citoyenneté israélienne et donc, en principe, des mêmes droits politiques et sociaux que ceux des israéliens juifs. Toutefois, en raison de diverses dispositions administratives subtiles, les localités majoritairement arabes d’Israël n’ont pas le même accès aux ressources financières du gouvernement que les municipalités juives. Néanmoins, la plupart des Palestiniens chrétiens se sont accommodés de l’État juif, apprécient les acquis sociaux, profitent de la situation économique d’Israël et jouissent de la liberté de voyager avec un passeport israélien. Ils s’engagent dans les partis arabes israéliens, sans pourtant se sentir liés, dans les élections, aux partis arabes. Ils votent aussi, selon les circonstances politiques, pour des partis majoritairement juifs de gauche et de droite, voire dans certains cas pour des partis juifs résolument religieux. Le processus d’intégration des chrétiens de Galilée dans l’État juif a commencé dès les années 1960. Aujourd’hui, rares sont les chrétiens de Galilée qui souhaiteraient échanger leur citoyenneté israélienne contre l’intégration dans un État palestinien, malgré la méfiance croissante de la population juive à l’égard des chrétiens à cause de la présentation biaisée du christianisme dans les écoles qui mettent un accent particulier sur la persécution des juifs dans les pays « chrétiens » pendant le Moyen-Âge et dans l’époque moderne et qui ne distinguent pas entre les chrétientés d’Occident et d’Orient. De nombreux chrétiens israéliens arabes sont préoccupés aussi par la propagation des idées islamistes au sein d’une partie de la population musulmane d’Israël. Cela a entraîné un fort recul de l’engagement politique commun entre chrétiens et musulmans. Les conflits entre musulmans, chrétiens et druzes sont également de plus en plus fréquents.
Au côté des chrétiens arabes d’Israël – et presque sans contact avec eux – vivent environ 420 000 Israéliens chrétiens de langue hébraïque. Ils sont principalement originaires des pays de l’ex-Union soviétique ainsi que des pays d’Europe de l’Est. La plupart d’entre eux sont russes orthodoxes. Ils sont tous citoyens israéliens et pleinement intégrés dans la société juive. S’y ajoutent environ 160 000 migrants chrétiens, dont beaucoup de femmes. Ceux-ci se composent de travailleurs migrants légaux et illégaux, originaires principalement d’Asie (Philippines, Inde, Sri Lanka) ; de demandeurs d’asile (surtout en provenance d’Érythrée et d’Éthiopie) ; de personnes qui, à la recherche d’un emploi, sont entrées avec un visa touristique déjà expiré (principalement d’Europe de l’Est, notamment de Roumanie et d’Ukraine). Les juifs convertis au christianisme constituent un groupe minuscule. Les chrétiens non-arabes installés de manière permanente en Israël représentent aujourd’hui environ un quart de la population chrétienne. Si l’on ajoute les travailleurs migrants et les demandeurs d’asile qui ne vivent que temporairement en Israël, ce groupe est même numériquement plus important que celui des chrétiens arabophones. Le plus grand groupe de migrants vit à Tel Aviv. C’est là qu’a été ouverte en 2015 une nouvelle église catholique avec un centre social pour les communautés de migrants. À Jérusalem, les migrants catholiques sont accueillis au centre « Ratisbonne » dans l’Ouest de la ville. De nombreuses communautés protestantes et évangéliques sont également actives en Israël. Leurs églises et lieux de culte sont souvent installés dans des magasins, des appartements et des abris anti-bombardement.
Les chrétiens représentent aujourd’hui près de 2 % de la population de l’État d’Israël (Jérusalem comprise). Si l’on y ajoute les migrants, ce chiffre atteint presque 4 %. Les juifs constituent 75 % de la population et les musulmans 18 %.
Telle est la complexité du christianisme en Israël. La loyauté envers l’État d’Israël, très répandue parmi les arabes chrétiens d’Israël, est régulièrement mise à l’épreuve. Les Palestiniens, chrétiens et musulmans de Cisjordanie, voient confirmé en ces occasions leur rejet par et de l’État juif. À titre d’exemple, citons la loi sur la nationalité adoptée par le Parlement israélien en 2018. Cette loi réaffirme le caractère juif de l’État, mais va encore plus loin en attribuant le droit à l’autodétermination nationale au seul peuple juif. Selon la nouvelle loi, la langue officielle est uniquement l’hébreu. L’arabe, qui est langue officielle depuis 1948, n’a plus qu’un statut particulier non défini. Certes, les conséquences pratiques de la loi sont marginales, puisqu’elle ne fait que confirmer ce qui va de soi dans l’esprit de la plupart des Juifs d’Israël. Elle n’en a pas moins un caractère hautement symbolique. C’est pourquoi elle a été vivement critiquée par les chefs d’Églises.
En mai 2021, le conflit déclenché par les expulsions de maisons palestiniennes dans le quartier arabe de Sheikh Jarrah à Jérusalem-Est et l’intervention musclée des forces de sécurité israéliennes lors de cérémonies du mois de Ramadan à la mosquée al-Aqsa ont profondément divisé les Juifs et les Arabes d’Israël. Du côté juif, on a eu peur des attaques de roquettes du Hamas. Du côté arabe, on était solidaire des victimes civiles des contre-attaques israéliennes à Gaza et des familles palestiniennes de Jérusalem-Est chassées de leurs maisons. Dans les villes mixtes d’Israël, où cohabitent Israéliens juifs et arabes, cela a donné lieu à de violentes émeutes et à des attaques lynchiennes de la part d’extrémistes juifs et arabes. Les gens des deux côtés avaient peur. Les chrétiens arabes d’Israël se sont retrouvés une fois de plus pris entre deux feux : solidarité avec le peuple palestinien dont ils font partie et loyauté envers l’État d’Israël, au sein des frontières dans lesquelles ils vivent. Les résultats des élections en Israël qui donnent des suffrages de plus en plus extrêmes et les annonces du gouvernement mises en place en décembre 2022 ne laissent présager rien de bon pour l’avenir de la cohabitation entre israéliens juifs et arabes de même que pour l’intégration des chrétiens arabes en Israël.
Palestine
Regardons encore la situation des chrétiens en Palestine, c’est-à-dire dans les territoires de Cisjordanie, administrés par l’Autorité palestinienne de Mahmoud Abbas, et dans la bande de Gaza, dirigée par un gouvernement Hamas. Y vivent environ 43 500 chrétiens (en 2008, des chiffres plus récents ne sont pas disponibles), dont moins de 1000 à Gaza. La population chrétienne de Cisjordanie se concentre dans la région de Bethléem avec Beit Jala et Beit Sahour ainsi qu’à Ramallah et dans les villages environnants. En Cisjordanie, les chrétiens représentent 1,5 % de la population parmi 98,5 % de musulmans. Dans la bande de Gaza, les chrétiens sont une infime minorité de moins de 0,1 % parmi une population presque entièrement musulmane. Les chrétiens sont pleinement intégrés dans la vie palestinienne et considèrent, pour la très grande majorité, l’État d’Israël et ses forces de sécurité comme des occupants. Ils souffrent beaucoup du blocus imposé par le mur de séparation qui coupe des territoires israéliens, les territoires contrôlés par l’Autorité palestinienne. De plus, les nombreux check-points israéliens font de la Cisjordanie « un patchwork » et rendent extrêmement long et compliqué le transport d’un endroit à l’autre. Dans ces conditions, les visites familiales, notamment aux nombreux chrétiens palestiniens vivant à Jérusalem, ne sont guère possibles, tout comme un contrat d’emploi en Israël. La bande de Gaza est même totalement isolée. De nombreux chrétiens de Palestine attribuent à la persistance du conflit israélo-palestinien, l’islamisation toujours plus poussée de la société palestinienne et de l’influence croissante de groupes islamistes extrémistes qui leur font peur.
Conclusions
Les Églises de Jérusalem peuvent-elles jouer un rôle de médiatrice pour la paix ? Le conflit au Proche-Orient n’est certes pas uniquement un conflit religieux. Mais les deux parties justifient leurs revendications en référence aux textes sacrés. Le conflit ne se comprend ni ne peut être résolu sans l’interférence de la religion. Certes, les référents religieux, du côté israélien et du côté palestinien ne sont pas les seuls, mais l’importance des revendications basées sur les arguments séculiers va en diminuant. Au cours des trois dernières décennies, l’essor du mouvement nationaliste religieux des colons juifs et la montée en puissance du Hamas, ont pris une ampleur angoissante. Cela ne manque pas d’avoir des répercussions sur la cohésion des Palestiniens chrétiens et musulmans. En fait, sans une participation constructive des religions, c’est-à-dire des leaders religieux et des organisations basées sur la foi religieuse, les tensions ne sauraient diminuer.
Quel rôle les Églises peuvent-elles jouer ? Au niveau mondial, les positions des Églises vis-à-vis du conflit israélo-arabe, sont loin d’être les mêmes. Beaucoup de chrétiens évangéliques américains soutiennent les revendications sionistes. Les Églises des pays arabes défendent le droit des Palestiniens. Le Vatican insiste sur le droit international et la décision de partage de l’ONU qui remonte à 1947. Il défend la position selon laquelle seuls Palestiniens et Israéliens ensemble peuvent parvenir à une autre solution par la voie de la négociation. Et l’Église de Jérusalem ? Elle aussi représente divers courants chrétiens : des chrétiens palestiniens en Palestine, des chrétiens arabes en Israël et des chrétiens de langue hébraïque en Israël, qui ont, chaque groupe pour sa part, des perspectives très différentes.
L’Église locale se trouve de plus en plus dans une situation de tension partagée entre les attentes des chrétiens de Palestine et de Jérusalem-Est d’une part et celles des chrétiens d’Israël d’autre part. Alors qu’en Palestine on attend que l’Église défende avec force les intérêts des Palestiniens, qu’elle dénonce les injustices et les violations du droit international, les Arabes israéliens s’identifient de plus en plus à l’État d’Israël et à ses réalisations sociales et économiques. La montée du Hamas et d’autres groupes islamistes à Gaza montre que les Églises pourraient jouer le rôle de médiateur. Les Églises doivent apprendre à gérer cette tension et les attentes divergentes de leurs fidèles. Elles pourraient ainsi jouer un rôle important de précurseur. La condition préalable est toutefois que les fossés confessionnels, particulièrement profonds en Terre Sainte pour des raisons historiques, soient enfin surmontés et que les Églises chrétiennes parviennent à une vraie entente œcuménique.

"""
    prompt = """Résume le texte ci-dessous en français. Le résumé doit faire environ 10% de l'article d'origine.
Output language: french
Text: $text
"""

    parameters = DeepInfraOpenAICompletionParameters(
        # model = "cognitivecomputations/dolphin-2.6-mixtral-8x7b",
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        max_tokens=512,
        completion_altText=None,
        prompt=prompt,
    )
    processor = DeepInfraOpenAICompletionProcessor()

    docs = processor.process([Document(text=text)], parameters=parameters)
    assert "Jerusalem" in docs[0].text


@pytest.mark.skip(reason="Not a test")
def test_explain_label():
    prompt = """Vous êtes un expert en classification de texte. Votre tâche consiste à fournir une explication en une phrase pour chacun des types d'événements décrits dans le texte en entrée.
La sortie doit être une table au format markdown dont la première colonne contient le type d'événement et la seconde colonne l'explication associée. Si aucun événement n'a été détecté, la sortie doit juste être "Aucun événement"
{%- set labels=[] -%}
{%- for cat in doc.categories -%}
  {%- do labels.append('"' + cat.label + '"') -%}
{%- endfor %}
{% if labels|length > 0 %}
Types d'événements à décrire: {{ labels|join(', ') }}
{%- else %}
Types d'événements à décrire: aucun
{%- endif %}
Texte: {{doc.text}}
    """
    parameters = OpenAICompletionParameters(
        model=OpenAIModel.gpt_3_5_turbo,
        completion_altText="explicationGPT",
        max_tokens=1024,
        prompt=prompt
    )
    processor = OpenAICompletionProcessor()

    parameters2 = DeepInfraOpenAICompletionParameters(
        model="cognitivecomputations/dolphin-2.6-mixtral-8x7b",
        completion_altText="explicationMixtral",
        max_tokens=1024,
        prompt=prompt,
    )
    processor2 = DeepInfraOpenAICompletionProcessor()

    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/event_detection-document-test.json",
    )
    with source.open("r") as fin:
        jdoc = json.load(fin)
        doc = Document(**jdoc)
        docs = processor.process([doc], parameters)
        doc1 = docs[0]
        assert doc1.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
        doc = Document(**jdoc)
        docs = processor2.process([doc], parameters2)
        doc2 = docs[0]
        assert doc2.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
