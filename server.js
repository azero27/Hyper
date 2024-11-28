const express = require("express");
const bodyParser = require('body-parser');
const { Gateway, Wallets } = require("fabric-network");
const path = require("path");
const fs = require("fs");

const app = express();
app.use(express.json()); // JSON 파싱

// Hyperledger Fabric 네트워크와 연결하는 함수
async function connectToNetwork() {
  const ccpPath = path.resolve(__dirname, '..', 'fabric-samples', 'test-network', 'organizations', 'peerOrganizations', 'org1.example.com', 'connection-org1.json');
  // 연결 파일 경로
  const ccp = JSON.parse(fs.readFileSync(ccpPath, "utf8"));

  const walletPath = path.join(process.cwd(), "wallet"); // 지갑 경로
  const wallet = await Wallets.newFileSystemWallet(walletPath);

  const gateway = new Gateway();
  await gateway.connect(ccp, {
    wallet,
    identity: "user1", // 네트워크에 접근할 사용자 ID
    discovery: { enabled: true, asLocalhost: true },
  });

  const network = await gateway.getNetwork("mychannel");
  const contract = network.getContract("basic");
  // 체인코드 이름이 'basic'인 경우
  return contract;
}

// 데이터 전송 API 엔드포인트
app.post('/submitData', async (req, res) => {
    try {
        const { id, ip, data } = req.body;
        const contract = await connectToNetwork();

        const result = await contract.submitTransaction('createTransaction', id, ip, data.toString());
        res.status(200).json({ blockCreationStatus: result.toString() });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(3000, () => {
    console.log('API 서버가 포트 3000에서 실행 중입니다.');
});