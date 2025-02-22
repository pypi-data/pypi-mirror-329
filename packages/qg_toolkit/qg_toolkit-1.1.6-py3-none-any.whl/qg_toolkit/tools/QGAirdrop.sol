// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract QGAirdrop {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    // 任何人都可以调用的批量空投方法
    function airdrop(address[] calldata recipients, uint256[] calldata amounts) external payable {
        require(recipients.length == amounts.length, "QG Error:Recipients and amounts arrays must have the same length");

        uint256 totalAmount = 0;

        // 计算总的空投数量
        for (uint256 i = 0; i < amounts.length; i++) {
            totalAmount += amounts[i];
        }

        // 校验发送的ETH数量是否和总空投数量相等
        require(msg.value == totalAmount, "QG Error:ETH value sent does not match the total airdrop amount");

        // 执行空投
        for (uint256 i = 0; i < recipients.length; i++) {
            payable(recipients[i]).transfer(amounts[i]);
        }
    }

    // 提现合约内的ETH, 任何人都可以调用
    function withdraw() external {
        payable(msg.sender).transfer(address(this).balance);
    }
}
