/* generated vector header file - do not edit */
        #ifndef VECTOR_DATA_H
        #define VECTOR_DATA_H
        #include "bsp_api.h"

        /** Common macro for FSP header files. There is also a corresponding FSP_FOOTER macro at the end of this file. */
        FSP_HEADER

                /* Number of interrupts allocated */
        #ifndef VECTOR_DATA_IRQ_COUNT
        #define VECTOR_DATA_IRQ_COUNT    (7)
        #endif
        /* ISR prototypes */
        void usbfs_interrupt_handler(void);
        void r_usb_dmaca_intDMAC0I_isr(void);
        void r_usb_dmaca_intDMAC1I_isr(void);
        void sci_uart_eri_isr(void);
        void sci_uart_rxi_isr(void);
        void sci_uart_txi_isr(void);
        void sci_uart_tei_isr(void);

        /* Vector table allocations */
        #define VECTOR_NUMBER_USB_FI ((IRQn_Type) 285) /* USB_FI (USB (Function) interrupt) */
        #define VECTOR_NUMBER_USB_FDMA0 ((IRQn_Type) 286) /* USB_FDMA0 (USB (Function) DMA 0 transmit completion) */
        #define VECTOR_NUMBER_USB_FDMA1 ((IRQn_Type) 287) /* USB_FDMA1 (USB (Function) DMA 1 transmit completion) */
        #define VECTOR_NUMBER_SCI0_ERI ((IRQn_Type) 288) /* SCI0_ERI (SCI0 Receive error) */
        #define VECTOR_NUMBER_SCI0_RXI ((IRQn_Type) 289) /* SCI0_RXI (SCI0 Receive data full) */
        #define VECTOR_NUMBER_SCI0_TXI ((IRQn_Type) 290) /* SCI0_TXI (SCI0 Transmit data empty) */
        #define VECTOR_NUMBER_SCI0_TEI ((IRQn_Type) 291) /* SCI0_TEI (SCI0 Transmit end) */
        typedef enum IRQn {
            SoftwareGeneratedInt0 = -32,
            SoftwareGeneratedInt1 = -31,
            SoftwareGeneratedInt2 = -30,
            SoftwareGeneratedInt3 = -29,
            SoftwareGeneratedInt4 = -28,
            SoftwareGeneratedInt5 = -27,
            SoftwareGeneratedInt6 = -26,
            SoftwareGeneratedInt7 = -25,
            SoftwareGeneratedInt8 = -24,
            SoftwareGeneratedInt9 = -23,
            SoftwareGeneratedInt10 = -22,
            SoftwareGeneratedInt11 = -21,
            SoftwareGeneratedInt12 = -20,
            SoftwareGeneratedInt13 = -19,
            SoftwareGeneratedInt14 = -18,
            SoftwareGeneratedInt15 = -17,
            DebugCommunicationsChannelInt = -10,
            PerformanceMonitorCounterOverflowInt = -9,
            CrossTriggerInterfaceInt = -8,
            VritualCPUInterfaceMaintenanceInt = -7,
            HypervisorTimerInt = -6,
            VirtualTimerInt = -5,
            NonSecurePhysicalTimerInt = -2,
            USB_FI_IRQn = 285, /* USB_FI (USB (Function) interrupt) */
            USB_FDMA0_IRQn = 286, /* USB_FDMA0 (USB (Function) DMA 0 transmit completion) */
            USB_FDMA1_IRQn = 287, /* USB_FDMA1 (USB (Function) DMA 1 transmit completion) */
            SCI0_ERI_IRQn = 288, /* SCI0_ERI (SCI0 Receive error) */
            SCI0_RXI_IRQn = 289, /* SCI0_RXI (SCI0 Receive data full) */
            SCI0_TXI_IRQn = 290, /* SCI0_TXI (SCI0 Transmit data empty) */
            SCI0_TEI_IRQn = 291, /* SCI0_TEI (SCI0 Transmit end) */
            SHARED_PERIPHERAL_INTERRUPTS_MAX_ENTRIES = BSP_VECTOR_TABLE_MAX_ENTRIES
        } IRQn_Type;

        /** Common macro for FSP header files. There is also a corresponding FSP_HEADER macro at the top of this file. */
        FSP_FOOTER

        #endif /* VECTOR_DATA_H */