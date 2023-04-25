# GaloisBlocks Cartesi
Cartesi code backend for the GaloisBlocks dApp build on the Cartesi Hackathon 2023 #BUIDLwithCartesi


![image](https://user-images.githubusercontent.com/33973526/231945244-7c48d004-82be-4ce0-babf-f61e6bb3ce0b.png)

Important steps for demo: 
Install ganache with 

```npm install ganache-cli --global```

And then run in port 9545 with:
```ganache -p 9545 ```

First build the rollup 
```docker buildx bake --load ```

Then run Cartesi Dapp as host-mode 
``` docker compose -f ../docker-compose.yml -f ./docker-compose.override.yml -f ../docker-compose-host.yml up ```

And in another terminal execute application backend 
``` ROLLUP_HTTP_SERVER_URL="http://127.0.0.1:5004" python3 ```

In another terminal run frontend-console and test the rollup with given examples in cartesiRollup.py
```
# Example 1: "NFT MyNFT MNFT 0x9fFC0375FF244F83877bb2fe47b1bbbE4ab37c25 100"
# Example 2: "DAO GB_DAOToken GBTkn 0x9fFC0375FF244F83877bb2fe47b1bbbE4ab37c25 3600"
# Example 3: "ERC20 GB_Token GBT 0x9fFC0375FF244F83877bb2fe47b1bbbE4ab37c25 1000"
```
