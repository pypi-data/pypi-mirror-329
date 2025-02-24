from enum import Enum,IntEnum

class Chip(Enum):
    bm1684x = 1
    bm1688 = 2
    bm1690 = 3
    sg2380 = 4
    sg2262 = 5
    mars3 = 6
    bm1684xe = 7

Chip.bm1684x.str = "bm1684x"
Chip.bm1688.str = "bm1688"
Chip.bm1690.str = "bm1690"
Chip.sg2262.str = "sg2262"
Chip.sg2380.str = "sg2380"
Chip.mars3.str = "mars3"
Chip.bm1684xe.str = "bm1684xe"

class ErrorCode(IntEnum):
    PplLocalAddrAssignErr = 0x11,
    FileErr = 0x12,
    LlvmFeErr = 0x13,
    PplFeErr = 0x14,
    PplOpt1Err = 0x15,
    PplOpt2Err = 0x16,
    PplFinalErr = 0x17,
    PplTransErr = 0x18,
    EnvErr = 0x19,
    PplL2AddrAssignErr = 0x1A,
    PplShapeInferErr = 0x1B,
    PplSetMemRefShapeErr = 0x1C,
    ToPplErr = 0x1D,
    PplTensorConvErr = 0x1E,
    PplDynBlockErr = 0x1F,
