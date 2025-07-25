/*
* Copyright (c) 2020 - 2025 Renesas Electronics Corporation and/or its affiliates
*
* SPDX-License-Identifier: BSD-3-Clause
*/

/***********************************************************************************************************************
 * Includes   <System Includes> , "Project Includes"
 **********************************************************************************************************************/
#include "bsp_api.h"

/***********************************************************************************************************************
 * Macro definitions
 **********************************************************************************************************************/
#define BSP_HACTLR_BIT_L                    (0xB783)     /* HACTLR EL1 access enable(0b1011 0111 1000 0011) */
#define BSP_HCR_HCD_DISABLE                 (0x20000000) /* HCR.HCD = 1 : HVC disable */
#define BSP_MODE_MASK                       (0x1F)       /* Bit mask for mode bits in CPSR */
#define BSP_SVC_MODE                        (0x13)       /* Supervisor mode */

#if defined(__ICCARM__)
 #define BSP_IRQ_STACK_END_ADDRESS          __section_end(".irq_stack")
 #define BSP_FIQ_STACK_END_ADDRESS          __section_end(".fiq_stack")
 #define BSP_SVC_STACK_END_ADDRESS          __section_end(".svc_stack")
 #define BSP_ABORT_STACK_END_ADDRESS        __section_end(".abt_stack")
 #define BSP_UNDEFINED_STACK_END_ADDRESS    __section_end(".und_stack")
 #define BSP_SYSTEM_STACK_END_ADDRESS       __section_end(".sys_stack")

#elif defined(__GNUC__)
 #define BSP_IRQ_STACK_END_ADDRESS          &__IrqStackLimit
 #define BSP_FIQ_STACK_END_ADDRESS          &__FiqStackLimit
 #define BSP_SVC_STACK_END_ADDRESS          &__SvcStackLimit
 #define BSP_ABORT_STACK_END_ADDRESS        &__AbtStackLimit
 #define BSP_UNDEFINED_STACK_END_ADDRESS    &__UndStackLimit
 #define BSP_SYSTEM_STACK_END_ADDRESS       &__SysStackLimit

#endif

#if (0 == BSP_CFG_CORE_CR52)
 #define BSP_IMP_BTCMREGIONR_MASK_L         (0x1FFC) /* Masked out BASEADDRESS and ENABLEELx bits(L) */
 #define BSP_IMP_BTCMREGIONR_ENABLEEL_L     (0x0003) /* Set base address and enable EL2, EL1, EL0 access(L) */
 #define BSP_IMP_BTCMREGIONR_ENABLEEL_H     (0x0010) /* Set base address and enable EL2, EL1, EL0 access(H) */

/* Cortex-A55 Core0 access permission control. */
 #define BSP_CA550_CTRL_ENABLE              (0x00000100)
#endif

/***********************************************************************************************************************
 * Typedef definitions
 **********************************************************************************************************************/

/***********************************************************************************************************************
 * Exported global variables (to be accessed by other files)
 **********************************************************************************************************************/
#if defined(__ICCARM__)
 #pragma section=".irq_stack"
 #pragma section=".fiq_stack"
 #pragma section=".svc_stack"
 #pragma section=".abt_stack"
 #pragma section=".und_stack"
 #pragma section=".sys_stack"

#elif defined(__GNUC__)
extern void * __IrqStackLimit;
extern void * __FiqStackLimit;
extern void * __SvcStackLimit;
extern void * __AbtStackLimit;
extern void * __UndStackLimit;
extern void * __SysStackLimit;

#endif

/***********************************************************************************************************************
 * Exported global functions (to be accessed by other files)
 **********************************************************************************************************************/
#if __FPU_USED
extern void bsp_fpu_advancedsimd_init(void);

#endif

#if (0 == BSP_CFG_CORE_CR52)
extern void bsp_slavetcm_enable(void);

#endif

/***********************************************************************************************************************
 * Private global variables and functions
 **********************************************************************************************************************/
int32_t main(void);

BSP_TARGET_ARM BSP_ATTRIBUTE_STACKLESS void system_init(void) BSP_PLACE_IN_SECTION(".loader_text");
BSP_TARGET_ARM BSP_ATTRIBUTE_STACKLESS void stack_init(void);
BSP_TARGET_ARM void                         fpu_slavetcm_init(void);

BSP_TARGET_ARM BSP_ATTRIBUTE_STACKLESS void        __Vectors(void) BSP_PLACE_IN_SECTION(".intvec");
__WEAK BSP_TARGET_ARM BSP_ATTRIBUTE_STACKLESS void IRQ_Handler(void);
__WEAK BSP_TARGET_ARM BSP_ATTRIBUTE_STACKLESS void Reset_Handler(void) BSP_PLACE_IN_SECTION(".reset_handler");

void Default_Handler(void);

/* Stacks */
BSP_DONT_REMOVE static uint8_t g_fiq_stack[BSP_CFG_STACK_FIQ_BYTES] BSP_ALIGN_VARIABLE(BSP_STACK_ALIGNMENT)
BSP_PLACE_IN_SECTION(BSP_SECTION_FIQ_STACK);
BSP_DONT_REMOVE static uint8_t g_irq_stack[BSP_CFG_STACK_IRQ_BYTES] BSP_ALIGN_VARIABLE(BSP_STACK_ALIGNMENT)
BSP_PLACE_IN_SECTION(BSP_SECTION_IRQ_STACK);
BSP_DONT_REMOVE static uint8_t g_abt_stack[BSP_CFG_STACK_ABT_BYTES] BSP_ALIGN_VARIABLE(BSP_STACK_ALIGNMENT)
BSP_PLACE_IN_SECTION(BSP_SECTION_ABT_STACK);
BSP_DONT_REMOVE static uint8_t g_und_stack[BSP_CFG_STACK_UND_BYTES] BSP_ALIGN_VARIABLE(BSP_STACK_ALIGNMENT)
BSP_PLACE_IN_SECTION(BSP_SECTION_UND_STACK);
BSP_DONT_REMOVE static uint8_t g_sys_stack[BSP_CFG_STACK_SYS_BYTES] BSP_ALIGN_VARIABLE(BSP_STACK_ALIGNMENT)
BSP_PLACE_IN_SECTION(BSP_SECTION_SYS_STACK);
BSP_DONT_REMOVE static uint8_t g_svc_stack[BSP_CFG_STACK_SVC_BYTES] BSP_ALIGN_VARIABLE(BSP_STACK_ALIGNMENT)
BSP_PLACE_IN_SECTION(BSP_SECTION_SVC_STACK);

/* Heap */
#if (BSP_CFG_HEAP_BYTES > 0)

BSP_DONT_REMOVE static uint8_t g_heap[BSP_CFG_HEAP_BYTES] BSP_ALIGN_VARIABLE(BSP_STACK_ALIGNMENT) \
    BSP_PLACE_IN_SECTION(BSP_SECTION_HEAP);
#endif

BSP_TARGET_ARM BSP_ATTRIBUTE_STACKLESS void __Vectors (void)
{
    __asm volatile (
        "    LDR pc,=Reset_Handler            \n"
        "    LDR pc,=Undefined_Handler        \n"
        "    LDR pc,=SVC_Handler              \n"
        "    LDR pc,=Prefetch_Handler         \n"
        "    LDR pc,=Abort_Handler            \n"
        "    LDR pc,=Reserved_Handler         \n"
        "    LDR pc,=IRQ_Handler              \n"
        "    LDR pc,=FIQ_Handler              \n"
        ::: "memory");
}

/*******************************************************************************************************************//**
 * @addtogroup BSP_MCU
 * @{
 **********************************************************************************************************************/

/*******************************************************************************************************************//**
 * Default exception handler.
 **********************************************************************************************************************/
void Default_Handler (void)
{
    /** A error has occurred. The user will need to investigate the cause. Common problems are stack corruption
     *  or use of an invalid pointer. Use the Fault Status window in e2 studio or manually check the fault status
     *  registers for more information.
     */
    BSP_CFG_HANDLE_UNRECOVERABLE_ERROR(0);
}

/*******************************************************************************************************************//**
 * After boot processing, LSI starts executing here.
 **********************************************************************************************************************/
BSP_TARGET_ARM BSP_ATTRIBUTE_STACKLESS void system_init (void)
{
#if 1
    __asm volatile (
        "    mov   r0, #0                               \n"
        "    movw  r1, #0xf07f                    \n"
        "    movt  r1, #0x2fa                        \n"
        "software_loop:                              \n"
        "    adds  r0, #1                                 \n"
        "    cmp   r0, r1                                 \n"
        "    bne   software_loop                  \n"
        ::: "memory");
#endif
    __asm volatile (
        "set_hactlr:                              \n"
        "    MOVW  r0, %[bsp_hactlr_bit_l]        \n" /* Set HACTLR bits(L) */
        "    MOVT  r0, #0                         \n"
        "    MCR   p15, #4, r0, c1, c0, #1        \n" /* Write r0 to HACTLR */
        ::[bsp_hactlr_bit_l] "i" (BSP_HACTLR_BIT_L) : "memory");

    __asm volatile (
        "set_hcr:                                 \n"
        "    MRC   p15, #4, r1, c1, c1, #0        \n" /* Read Hyp Configuration Register */
        "    ORR   r1, r1, %[bsp_hcr_hcd_disable] \n" /* HVC instruction disable */
        "    MCR   p15, #4, r1, c1, c1, #0        \n" /* Write Hyp Configuration Register */
        ::[bsp_hcr_hcd_disable] "i" (BSP_HCR_HCD_DISABLE) : "memory");

    __asm volatile (
        "set_vbar:                                \n"
        "    LDR   r0, =__Vectors                 \n"
        "    MCR   p15, #0, r0, c12, c0, #0       \n" /* Write r0 to VBAR */
        ::: "memory");

#if (0 == BSP_CFG_CORE_CR52) || (1 == BSP_FEATURE_BSP_HAS_CR52_CPU1_LLPP)
    __asm volatile (
        "LLPP_access_enable:                      \n"

        /* Enable PERIPHPREGIONR (LLPP) */
        "    MRC   p15, #0, r1, c15, c0,#0        \n" /* PERIPHPREGIONR */
        "    ORR   r1, r1, #(0x1 << 1)            \n" /* Enable PERIPHPREGIONR EL2 */
        "    ORR   r1, r1, #(0x1)                 \n" /* Enable PERIPHPREGIONR EL1 and EL0 */
        "    DSB                                  \n" /* Ensuring memory access complete */
        "    MCR   p15, #0, r1, c15, c0,#0        \n" /* PERIPHREGIONR */
        "    ISB                                  \n" /* Ensuring Context-changing */
        ::: "memory");
#endif

    __asm volatile (
        "cpsr_save:                               \n"
        "    MRS   r0, CPSR                       \n" /* Original PSR value */
        "    BIC   r0, r0, %[bsp_mode_mask]       \n" /* Clear the mode bits */
        "    ORR   r0, r0, %[bsp_svc_mode]        \n" /* Set SVC mode bits */
        "    MSR   SPSR_hyp, r0                   \n"
        ::[bsp_mode_mask] "i" (BSP_MODE_MASK), [bsp_svc_mode] "i" (BSP_SVC_MODE) : "memory");

    __asm volatile (
        "exception_return:                        \n"
        "    LDR   r1, =stack_init                \n"
        "    MSR   ELR_hyp, r1                    \n"
        "    ERET                                 \n" /* Branch to stack_init and enter EL1 */
        ::: "memory");
}

/** @} (end addtogroup BSP_MCU) */

#if defined(__ICCARM__)
 #define BSP_SYSTEMINIT_B_INSTRUCTION    SystemInit();

 #define WEAK_REF_ATTRIBUTE

 #pragma weak Undefined_Handler     = Default_Handler
 #pragma weak SVC_Handler           = Default_Handler
 #pragma weak Prefetch_Handler      = Default_Handler
 #pragma weak Abort_Handler         = Default_Handler
 #pragma weak Reserved_Handler      = Default_Handler
 #pragma weak FIQ_Handler           = Default_Handler
#elif defined(__GNUC__)

 #define BSP_SYSTEMINIT_B_INSTRUCTION    __asm volatile ("B SystemInit");

 #define WEAK_REF_ATTRIBUTE              __attribute__((weak, alias("Default_Handler")))
#endif

void Undefined_Handler(void) WEAK_REF_ATTRIBUTE;
void SVC_Handler(void) WEAK_REF_ATTRIBUTE;
void Prefetch_Handler(void) WEAK_REF_ATTRIBUTE;
void Abort_Handler(void) WEAK_REF_ATTRIBUTE;
void Reserved_Handler(void) WEAK_REF_ATTRIBUTE;
void FIQ_Handler(void) WEAK_REF_ATTRIBUTE;

/*******************************************************************************************************************//**
 * After system_init, EL1 settings start here.
 **********************************************************************************************************************/
BSP_TARGET_ARM BSP_ATTRIBUTE_STACKLESS void stack_init (void)
{
    __asm volatile (
        "stack_initialization:                           \n"

        /* Stack setting for EL1 */
        "    CPS  #17                                    \n" /* FIQ mode */
        "    MOV  sp, %[bsp_fiq_stack_end_address]       \n"
        "    CPS  #18                                    \n" /* IRQ mode */
        "    MOV  sp, %[bsp_irq_stack_end_address]       \n"
        "    CPS  #23                                    \n" /* Abort mode */
        "    MOV  sp, %[bsp_abort_stack_end_address]     \n"
        "    CPS  #27                                    \n" /* Undefined mode */
        "    MOV  sp, %[bsp_undefined_stack_end_address] \n"
        "    CPS  #31                                    \n" /* System mode */
        "    MOV  sp, %[bsp_system_stack_end_address]    \n"
        "    CPS  #19                                    \n" /* SVC mode */
        "    MOV  sp, %[bsp_svc_stack_end_address]       \n"

        "    B    fpu_slavetcm_init                      \n" /* Branch to fpu_slavetcm_init */
        ::[bsp_fiq_stack_end_address] "r" (BSP_FIQ_STACK_END_ADDRESS),
        [bsp_irq_stack_end_address] "r" (BSP_IRQ_STACK_END_ADDRESS),
        [bsp_abort_stack_end_address] "r" (BSP_ABORT_STACK_END_ADDRESS),
        [bsp_undefined_stack_end_address] "r" (BSP_UNDEFINED_STACK_END_ADDRESS),
        [bsp_system_stack_end_address] "r" (BSP_SYSTEM_STACK_END_ADDRESS),
        [bsp_svc_stack_end_address] "r" (BSP_SVC_STACK_END_ADDRESS) : "memory");
}

/*******************************************************************************************************************//**
 * Enable FPU and enable privileged/unprivileged access for TCM.
 **********************************************************************************************************************/
BSP_TARGET_ARM void fpu_slavetcm_init (void)
{
#if __FPU_USED

    /* Initialize FPU and Advanced SIMD setting */
    bsp_fpu_advancedsimd_init();
#endif

#if (0 == BSP_CFG_CORE_CR52)

    /* Enable SLAVEPCTLR TCM access lvl slaves */
    bsp_slavetcm_enable();
#endif

#if defined(BSP_MCU_GROUP_RZN2H)
 #if (0 == BSP_CFG_CORE_CR52)

    /* Permit access to the Master-MPU related registers of Cortex-A55 Core0. */
    R_MPU_AC->CPU_CTRL |= BSP_CA550_CTRL_ENABLE;
 #endif
#endif

    BSP_SYSTEMINIT_B_INSTRUCTION
}

__WEAK BSP_TARGET_ARM BSP_ATTRIBUTE_STACKLESS void IRQ_Handler (void)
{
    __asm volatile (
        "SUB     lr, lr, #4                       \n"
        "SRSDB   sp!, #31                         \n" /* Store LR_irq and SPSR_irq in system mode stack. */
        "CPS     #31                              \n" /* Switch to system mode. */
        "PUSH    {r0-r3, r12}                     \n" /* Store other AAPCS registers. */

#if __FPU_USED
        "VMRS    r0, FPSCR                        \n"
        "STMDB   sp!, {r0}                        \n" /* Store FPSCR register. */
        "SUB     sp, sp, #4                       \n"
        "VPUSH   {d0-d15}                         \n" /* Store FPU registers. */
        "VPUSH   {d16-d31}                        \n" /* Store FPU registers. */
#endif

        "MRC     p15, #0, r3, c12, c12, #2        \n" /* Read HPPIR1 to r3. */
        "MRC     p15, #0, r0, c12, c12, #0        \n" /* Read IAR1 to r0. */

        "PUSH    {r0}                             \n" /* Store the INTID. */
        "MOV     r1, sp                           \n" /* Make alignment for stack. */
        "AND     r1, r1, #4                       \n"
        "SUB     sp, sp, r1                       \n"
        "PUSH    {r1, lr}                         \n"

        "LDR     r1,=bsp_common_interrupt_handler \n"
        "BLX     r1                               \n" /* Jump to bsp_common_interrupt_handler, First argument (r0) = ICC_IAR1 read value. */

        "POP     {r1, lr}                         \n"
        "ADD     sp, sp, r1                       \n"
        "POP     {r0}                             \n" /* Restore the INTID to r0. */

        "MCR     p15, #0, r0, c12, c12, #1        \n" /* Write INTID to EOIR. */

#if __FPU_USED
        "VPOP    {d16-d31}                        \n" /* Restore FPU registers. */
        "VPOP    {d0-d15}                         \n" /* Restore FPU registers. */
        "ADD     sp, sp, #4                       \n"
        "POP     {r0}                             \n"
        "VMSR    FPSCR, r0                        \n" /* Restore FPSCR register. */
#endif

        "POP     {r0-r3, r12}                     \n" /* Restore registers. */
        "RFEIA   sp!                              \n" /* Return from system mode tack using RFE. */
        ::: "memory");
}

__WEAK BSP_TARGET_ARM BSP_ATTRIBUTE_STACKLESS void Reset_Handler (void)
{
#if (0 == BSP_CFG_CORE_CR52)

    /* Enable access to BTCM */
    __asm volatile (
        "set_IMP_BTCMREGIONR:                            \n"
        "   MRC   p15, #0, r0, c9, c1, #1                \n" /* Read IMP_BTCMREGIONR to r0 */
        "   MOVW  r1, %[bsp_imp_btcmregionr_mask_l]      \n"
        "   MOVT  r1, #0                                 \n"
        "   AND   r0, r0, r1                             \n" /* Masked out BASEADDRESS and ENABLEELx bits */
        "   MOVW  r1, %[bsp_imp_btcmregionr_enableel_l]  \n"
        "   MOVT  r1, %[bsp_imp_btcmregionr_enableel_h]  \n"
        "   ORR   r0, r0, r1                             \n" /* Set base address and enable EL2, EL1, EL0 access */
        "   DSB                                          \n" /* Ensuring memory access complete */

        "   MCR   p15, #0, r0, c9, c1, #1                \n" /* Write r0 to IMP_BTCMREGIONR */
        "   ISB                                          \n" /* Ensuring Context-changing */
        ::[bsp_imp_btcmregionr_mask_l] "i" (BSP_IMP_BTCMREGIONR_MASK_L),
        [bsp_imp_btcmregionr_enableel_l] "i" (BSP_IMP_BTCMREGIONR_ENABLEEL_L),
        [bsp_imp_btcmregionr_enableel_h] "i" (BSP_IMP_BTCMREGIONR_ENABLEEL_H) : "memory");
#endif

    /* Branch to system_init */
    __asm volatile ("B system_init");
}
