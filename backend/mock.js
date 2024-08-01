const Mock = require('mockjs');
const params = JSON.parse(process.argv[2]); // 读取命令行传递的第二个参数

function generateMockData(params) {
    const data = Mock.mock(params);
    return JSON.stringify(data);
}

const generatedData = generateMockData(params);
console.log(generatedData);