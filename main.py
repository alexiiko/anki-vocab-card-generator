from bs4 import BeautifulSoup
import requests

url = "https://read.amazon.com/notebook?openid.assoc_handle=amzn_kp_us&openid.claimed_id=https%3A%2F%2Fwww.amazon.com%2Fap%2Fid%2Famzn1.account.AGDR7N7DXQEOS3RM27IFDYKO3DEA&openid.identity=https%3A%2F%2Fwww.amazon.com%2Fap%2Fid%2Famzn1.account.AGDR7N7DXQEOS3RM27IFDYKO3DEA&openid.mode=id_res&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.op_endpoint=https%3A%2F%2Fwww.amazon.com%2Fap%2Fsignin&openid.response_nonce=2023-05-08T13%3A02%3A12Z4248070967486381231&openid.return_to=https%3A%2F%2Fread.amazon.com%2Fnotebook&openid.signed=assoc_handle%2Cclaimed_id%2Cidentity%2Cmode%2Cns%2Cop_endpoint%2Cresponse_nonce%2Creturn_to%2Cns.pape%2Cpape.auth_policies%2Cpape.auth_time%2Csigned&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.auth_policies=http%3A%2F%2Fschemas.openid.net%2Fpape%2Fpolicies%2F2007%2F06%2Fnone&openid.pape.auth_time=2023-05-08T13%3A02%3A12Z&openid.sig=dYEqY6XsxHTYHztcHNhh2IXvb2SfH7c2jPjcJt6prMg%3D&serial="

response = requests.get(url)

scraper = BeautifulSoup(response.text, "html.parser")

span_vocab_class = scraper.find(id="highlight")


for vocab in span_vocab_class:
    print(vocab.text)

print(span_vocab_class)
