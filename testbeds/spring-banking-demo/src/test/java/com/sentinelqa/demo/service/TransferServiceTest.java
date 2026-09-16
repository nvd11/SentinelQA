package com.sentinelqa.demo.service;

import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import static org.assertj.core.api.Assertions.assertThat;

class TransferServiceTest {

    @Test
    void testBasicTransferHappyPath() {
        TransferService service = new TransferService();
        boolean result = service.transferFunds("ACC-001", "ACC-002", new BigDecimal("100.00"));
        assertThat(result).isTrue();
    }
}
