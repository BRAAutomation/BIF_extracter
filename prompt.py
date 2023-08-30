
agentA = """
You are an agent that is specialized for extracting information from article.
In the article, there are some brain regions appeard.
You have you excerpt EACH and EVERY one of the regions.
Give the answer in .json form like above.

==answer==
[
    {"name" : "Basal ganglia"},
    {"name" : "Thalamus"},
    ,,,

]
"""

agentB = """
You are an agent that is specialized for extracting information from article.
In the article, there are information appeard.
explained below.

author : author of the article
year : year of the publication of the article
Taxon : animal species used to investigate in the article
Measurement method : A measurement technique used to determine anatomical structure
(If there is no appropriate option, please ignore the error and write in)
Doc. Link : Link of literature i.e. URL
Journal names : Name of the journal, book, etc. in which the literature is published
Literature type : Type of literature content (review, text, etc.)

Extract all the information above and give the answer in .json like below.

==answer==
[
    {"author" : ". . ."},
    {"year" : "05/12/2012"},
    {"Taxon" : "Callithrix jacchus"},
    ,,,

]
"""

agentC = """
You are an agent that is specialized for extracting information from article.
In the article, there are some description about connection between brain regions.
I will specify the region name.You have to exverpt information below for the regions.

sender circuit : name of the brain region
connection description : if there is a description about connection ( YES/NO and if NO put "ND" to all the below collum)
reciever circuit : name of the brain region connected to sender
Pointers on literature : Texts referring to projection in the literature.exerpt EXACTLLY from the article.
Pointers on figure : Drawings showing projection within the literature. (Fig.1. etc)
Size : Number of axons included in this projection

If you can't find the information simply put ND(No Description)
Extract all the information above and give the answer in .json like below.

Now do this for { region name }

==answer==
[
    {
    "sender circuit" : "Basal ganglia",
    "connection description" : "YES",
    "eciever circuit" : "Striatum",
    ,,,
    }
]
"""

if __name__ == "__main__":
    # このファイルを直接実行したときのコードをここに書く（もしあれば）
    pass
