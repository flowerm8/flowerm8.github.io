from flask import Flask, request, render_template, redirect
from blockfrost import BlockFrostApi, ApiError, ApiUrls

app = Flask(__name__)

@app.route("/pool.pm", methods=['GET'])
def redirect():
    link = request.args.get('link', '/')
    new_link = 'http://' + link
    print("redirected")
    return redirect("google.com")

@app.route("/", methods=['GET'])
def homePage():
    return render_template("websiteTest1.7.html")

@app.route("/", methods =["POST"])
def home():
    api = BlockFrostApi(
    project_id='mainnetzHEhgCG9dZKFO0YtoQXsOfPY2eEW9frj',  
    base_url=ApiUrls.mainnet.value,
)
    #dAsset = "dac355946b4317530d9ec0cb142c63a4b624610786c2a32137d78e2561646170654c616e64727943617374696c6c6f"
    #print(request.method)
    #if request.method == "POST":
    dAsset = request.form.get("desiredAsset")
    print("it worked")
    if "jpg.store" in dAsset:
        dAsset = dAsset.rsplit('/', 1)[1]
    #dAsset = request.args['desiredAsset']
    #print(dAsset)
    addresses = []
    try:

        #getting the minting address
        mintingAction = api.asset_history(
            asset = dAsset
        )
        #print(mintingAction)
        mintingAction = str(mintingAction)
        addrIndex3 = mintingAction.find("=")
        endAddrIndex3 = mintingAction.find(",")
        mintingTx = mintingAction[addrIndex3+2:endAddrIndex3-1]
        #print(mintingTx)
        mintingUtxo = api.transaction_utxos(
            hash = mintingTx
        )
        #print(mintingUtxo)
        mintingUtxo = str(mintingUtxo)
        #grabbing the first addy from the mint tx (im assuming it's the one that's minting)
        addrIndexMinting = mintingUtxo.find("inputs=[Namespace(address='")
        endAddrIndexMinting = mintingUtxo.find(",", addrIndexMinting)
        #print("----------------------------")
        #print(mintingUtxo[addrIndexMinting + 27 :endAddrIndexMinting-1])
        addresses.append(mintingUtxo[addrIndexMinting + 27 :endAddrIndexMinting-1])
        txs = api.asset_transactions(
            asset = dAsset
        )
        txsStr = str(txs)
        res = [i for i in range(len(txsStr)) if txsStr.startswith("tx_hash=", i)]
        txHashes = []
        for index in res:
            tx_hash = txsStr[index: index + 74]
            txHashes.append(tx_hash)
        utxos = []
        for hashx in txHashes:
            utxo = api.transaction_utxos(
                hash = hashx[9:73]
            )
            utxos.append(utxo)
        indices = []
        #wallets that the asset has touched
        for utxo in utxos:
            utxo = str(utxo)
            index = utxo.find(dAsset)
            addrIndex = utxo.rfind("Namespace(address='", 0, index)
            endAddrIndex = utxo.find(",", addrIndex)
            addresses.append(utxo[addrIndex+19:endAddrIndex-1])
        currentDassetWallet = api.asset_addresses(
            asset = dAsset
        )
        #where the asset currently is
        addrIndex2 = str(currentDassetWallet).find("=")
        endAddrIndex2 = str(currentDassetWallet).find(",")
        addresses.append(str(currentDassetWallet)[addrIndex2+2:endAddrIndex2-1])
        addresses = [addresses[i] for i in range(len(addresses)) if (i==0) or addresses[i] != addresses[i-1]]
        print("---------------------------------------------------------------")
        print(addresses)

    except ApiError as e:
        print(e)
    #return addresses
    #return render_template("websiteTest1.6.html"), addresses
    #return addresses
    #return render_template("websiteTest1.5.html")
    #return render_template("websiteTest1.5.html", dAsset=request.args['desiredAsset'])
    return render_template("index.html", addresses=addresses)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
