from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel,RunnableLambda,RunnablePassthrough

model=ChatMistralAI(model="mistral-small-2506")
parser=StrOutputParser()
code_prompt=ChatPromptTemplate.from_messages([
    ("system","You are a ai code generator in java language and short code "),
    ("user","{topic}"),
])
explain_prompt=ChatPromptTemplate.from_messages([
    ("system","You are a ai code generator in java language and short code "),
    ("user","Explain the code generated in simple words step by step:\n{code}"),
])
seq1=code_prompt|model|parser
seq2=RunnableParallel({
    "code":RunnablePassthrough(),
    "explanation":explain_prompt|model|parser,
})
pipeline=seq1|seq2
result=pipeline.invoke({
    "topic":"Write a code for generating all distinct palindrome strings in a string"
})

print(parser.parse(result['explanation']))
