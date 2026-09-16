package com.sentinelqa.demo.service;

import java.math.BigDecimal;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class TransferService {

    private final Map<String, BigDecimal> accountBalances = new ConcurrentHashMap<>();

    public TransferService() {
        accountBalances.put("ACC-001", new BigDecimal("1000.00"));
        accountBalances.put("ACC-002", new BigDecimal("500.00"));
    }

    public BigDecimal getBalance(String accountId) {
        return accountBalances.getOrDefault(accountId, BigDecimal.ZERO);
    }

    public boolean transferFunds(String fromAccount, String toAccount, BigDecimal amount) {
        if (amount == null || amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("Transfer amount must be positive");
        }

        BigDecimal currentFromBalance = getBalance(fromAccount);
        if (currentFromBalance.compareTo(amount) < 0) {
            return false; // Overdraft rejected
        }

        // Intentionally lacking synchronized lock or rollback for demo testing
        accountBalances.put(fromAccount, currentFromBalance.subtract(amount));
        BigDecimal currentToBalance = getBalance(toAccount);
        accountBalances.put(toAccount, currentToBalance.add(amount));

        return true;
    }
}
