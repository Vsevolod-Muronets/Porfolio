from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

my_credentials = {"url": "УДАЛЕНО ИЗ СООБРАЖЕНИЙ БЕЗОПАСНОСТИ"}

params = {GenParams.MAX_NEW_TOKENS: 700, GenParams.TEMPERATURE: 0.1}

LLAMA2_model = Model(
    model_id= 'meta-llama/llama-3-2-11b-vision-instruct',
    credentials=my_credentials, params=params, project_id="УДАЛЕНО ИЗ СООБРАЖЕНИЙ БЕЗОПАСНОСТИ"
    )

llm = WatsonxLLM(LLAMA2_model)

print(llm("How to read a book effectively?"))
