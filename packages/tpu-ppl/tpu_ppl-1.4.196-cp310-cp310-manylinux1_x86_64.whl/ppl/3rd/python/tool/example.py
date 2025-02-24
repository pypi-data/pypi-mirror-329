#!/usr/bin/env python3

Y, N = True, False

full_list = {
    # (filename,                                              bm1684x, bm1688, bm1690, sg2380, sg2262, masr3, bm1684xe)
    #                                                         [base, full]
    "regression/unittest/arith":
      [("arith_int.pl",                                          Y,       Y,      Y,      N,      Y,     N,     N),
       ("add_pipeline_bm1688.pl",                                N,       N,      N,      N,      N,     N,     N),],
    "regression/unittest/arith_int":
      [("c_sub_int.pl",                                          N,       N,      N,      N,      N,     N,     N),],
    "regression/unittest/attention":
      [("rotary_embedding_static.pl",                            N,       N,      N,      N,      N,     N,     N),
       ("mlp_left_trans_multicore.pl",                           N,       N,      Y,      N,      N,     N,     N)],
    "regression/unittest/cmp":
      [("greater_fp16.pl",                                       Y,       N,      N,      N,      N,     Y,     N),
       ("equal_int16.pl",                                        Y,       N,      N,      N,      N,     N,     N),],
    "regression/unittest/conv":
      [("Conv2D.pl",                                             Y,       N,      Y,      N,      N,     N,     N),
       ("depthwise2d_int8.pl",                                   Y,       N,    [N,Y],    N,      N,     N,     N),
       ("quant_conv2d_for_deconv2d_int8_asym_int16_int8.pl",     Y,       N,      Y,      N,      N,     N,     N),],
    "regression/unittest/divide":
      [("fp32_tunable_div_multi_core.pl",                        N,       N,      Y,      N,      N,     Y,     N),],
    "regression/unittest/dma":
      [("move_s2s_fp32.pl",                                    [N,Y],     N,      N,      N,      N,     N,     N),
       ("dmaload_bc_S2L_fp32.pl",                                N,       N,      N,      N,      N,     N,     N),
       ("dmaload_bc_L2L_fp32.pl",                                N,       N,      N,      N,      N,     N,     N),
       ("dma_nonzero_l2s.pl",                                  [N,Y],     N,      N,      N,      N,     N,     N),
       ("dma_nonzero_s2s.pl",                                  [N,Y],     N,      N,      N,      N,     N,     N),],
    "regression/unittest/gather_scatter":
      [("batch_bcast_w_scatter_fp16.pl",                       [N,Y],     N,      N,      N,      N,     N,     N),
       ("h_scatter_s2s_index_local_bf16.pl",                   [N,Y],     N,      N,      N,      N,     N,     N),
       ("hw_gather_bf16.pl",                                   [N,Y],     N,      N,      N,      N,     N,     N),
       ("hw_scatter_bf16.pl",                                  [N,Y],     N,      N,      N,      N,     N,     N),
       ("w_gather_bf16.pl",                                    [N,Y],     N,      N,      N,      N,     N,     N),
       ("w_scatter_bf16.pl",                                     Y,       N,      N,      N,      N,     N,     N),],
    "regression/unittest/hau":
      [("hau_sort_2d.pl",                                        N,       N,      N,      N,      N,     N,     N),
       ("topk.pl",                                               N,       N,      N,      N,      N,     N,     N),
       ("hau.pl",                                                Y,       N,      N,      N,      N,     N,     N),
       ("hau_poll.pl",                                           Y,       N,      Y,      N,      N,     N,     N),],
    "regression/unittest/mask":
      [("mask_select_batch_bcast_bf16_multi_core.pl",            Y,       N,      N,      N,      N,     N,     N),],
    "regression/unittest/matmul":
      [("mm2_int8_all_trans.pl",                               [N,Y],     N,      N,      N,      Y,     Y,     N),
       ("mm_fp32.pl",                                          [N,Y],     N,      N,      N,    [N,Y],   N,     N),],
    "regression/unittest/npu":
      [("npu_bcast_fp16.pl",                                   [N,Y],     N,      N,      N,    [N,Y],   N,     N),],
    "regression/unittest/round":
      [("round_bf16.pl",                                       [N,Y],     N,      N,      N,      N,     N,     N),],
    "regression/unittest/rqdq":
      [("rq_fp_int8_uint16.pl",                                  Y,     [N,Y],   [N,Y],   N,    [N,Y],   N,     N),],
    "regression/unittest/scalebias":
      [("fp_scale_bias_bf16.pl",                               [N,Y],     N,      N,      N,      N,     N,     N),],
    "regression/unittest/sdma":
      [("sdma.pl",                                               N,       N,      Y,      N,      N,     N,     N),],
    "regression/unittest/unary":[],
    "examples/cxx/arith":
      [("add_c_dual_loop.pl",                                    N,       N,      N,      N,      N,     N,     N),
       ("add_dyn_block.pl",                                      Y,       Y,      Y,      N,      N,     Y,     N),
       ("add_pipeline.pl",                                       N,       N,    [N,Y],    N,      N,     Y,     N),
       ("add_broadcast.pl",                                      N,       N,    [N,Y],    N,    [N,Y],   Y,     N),],
    "examples/cxx/llm":
      [("attention_dyn.pl",                                      Y,       Y,      Y,      N,      N,     N,     N),
       ("flash_attention.pl",                                    N,       N,      N,      N,      N,     N,     N),
       ("rmsnorm.pl",                                          [N,N],     N,      N,      N,      N,     N,     N),
       ("mlp_multicore.pl",                                      N,       N,      Y,      N,      N,     N,     N),
       ("swi_glu.pl",                                          [N,Y],     N,      N,      N,    [N,Y],   N,     N),
       ("flash_attention_backward_multicore.pl",                 N,       N,    [N,Y],    N,    [N,Y],   N,     N),
       ("flash_attention_GQA_multicore.pl",                      N,       N,      Y,      N,      Y,     N,     N),],
    "examples/cxx/llm/tgi":
      [("w4a16_matmul.pl",                                       N,       N,      Y,      N,      N,     N,     N),
       ("rmsnorm_small_row.pl",                                  N,       N,      Y,      N,      N,     N,     N)],
    "examples/cxx/matmul":
      [("mm2_fp16_sync.pl",                                      N,       N,      Y,      N,      N,     N,     N),
       ("mm.pl",                                               [N,Y],     N,      N,      N,      Y,     N,     N),
       ("mm2_int.pl",                                            Y,       N,      N,      N,      N,     N,     N),
       ("mm2_float.pl",                                          N,       N,      N,      N,      Y,     N,     N),],
    "regression/unittest/fileload":
      [("test_read.pl",                                          Y,       N,      N,      N,      N,     N,     N),],
    "regression/unittest/pool":
      [("avg_pool2d.pl",                                       [N,Y],     N,      N,      N,      N,     N,     N),],
    "examples/cxx/activation":
      [("softmax_h_dim.pl",                                      Y,       N,    [N,Y],    N,      N,     N,     N),],
    "regression/unittest/func":
      [("sin.pl",                                                Y,       N,      N,      N,      N,     N,     N),
       ("cos.pl",                                              [N,Y],     N,      N,      N,      N,     N,     N),
       ("arcsin.pl",                                           [N,Y],     N,      N,      N,      N,     N,     N),
       ("arccos.pl",                                           [N,Y],     N,      N,      N,      N,     N,     N),
       ("tan.pl",                                              [N,Y],     N,      N,      N,      N,     N,     N),
       ("cot.pl",                                                Y,       N,      N,      N,      N,     N,     N),
       ("sqrt.pl",                                             [N,Y],     N,      N,      N,    [Y,Y],   N,     N),
       ("sqrt_mars3_bf16.pl",                                  [N,Y],     N,      N,      N,      N,     Y,     N),
       ("relu.pl",                                             [N,Y],     N,      N,      N,      N,     N,     N),
       ("prelu.pl",                                            [N,Y],     N,      N,      N,      N,     N,     N),
       ("exp.pl",                                              [N,Y],     N,      N,      N,      N,     N,     N),
       ("softplus.pl",                                         [N,Y],     N,      N,      N,      N,     N,     N),
       ("mish.pl",                                             [N,Y],     N,      N,      N,      N,     N,     N),
       ("sinh.pl",                                             [N,Y],     N,      N,      N,      N,     N,     N),
       ("cosh.pl",                                             [N,Y],     N,      N,      N,      N,     N,     N),
       ("tanh.pl",                                             [N,Y],     N,      N,      N,      N,     N,     N),
       ("arcsinh.pl",                                          [N,Y],     N,      N,      N,      N,     N,     N),
       ("arccosh.pl",                                          [N,Y],     N,      N,      N,      N,     N,     N),
       ("arctanh.pl",                                          [N,Y],     N,      N,      N,      N,     N,     N),
       ("softsign.pl",                                         [N,Y],     N,      N,      N,      N,     N,     N),],
}

sample_list = {
    # (filename,                      bm1684x, bm1688, bm1690, sg2380, sg2262, mars3, bm1684xe)
    "samples/add_pipeline":
      [("test",                         Y,       N,      Y,      N,      N,      N,      N),],
    "samples/llama2":
      [("test",                         Y,       N,      N,      N,      N,      N,      N),],
    "regression/unittest/torch_tpu":
      [("test",                         N,       N,      Y,      N,      N,      N,      N),],
    "regression/unittest/tpu_mlir":
      [("test",                         Y,       N,      N,      N,      N,      N,      N),],
}

python_list = {
    # (filename,                      bm1684x, bm1688, bm1690, sg2380, sg2262, mars3, bm1684xe)
    "examples/python":
      [("01-element-wise.py",            Y,       Y,      Y,      N,      Y,     N,     N),
       ("01-element-wise-bm1684x.py",    Y,       N,      N,      N,      N,     N,     N),
       ("02-avg-max-pool.py",            Y,       N,      N,      N,      N,     N,     N),
       ("02-min-pool.py",                N,       N,      N,      N,      N,     N,     N),
       ("03-conv.py",                    N,       N,      N,      N,      Y,     N,     N),
       ("03-conv-bm1688.py",             N,       N,      N,      N,      N,     N,     N),
       ("04-matmul.py",                  Y,       N,      N,      N,      N,     N,     N),
       ("04-matmul-bm1688.py",           N,       N,      N,      N,      N,     N,     N),
       ("05-attention-GQA.py",           Y,       N,      Y,      N,      Y,     N,     N),
       ("06-gather-scatter.py",          Y,       N,      N,      N,      N,     N,     N),
       ("07-arange_broadcast.py",        Y,       N,      N,      N,      N,     N,     N),
       ("09-dma.py",                     Y,       N,      N,      N,      N,     N,     N),
       ("10-vc-op.py",                   Y,       N,      N,      N,      N,     N,     N),
       ("11-tiu-transpose.py",           Y,       N,      N,      N,      N,     N,     N),
       ("13-hau.py",                     Y,       N,      N,      N,      N,     N,     N),
       ("14-sdma.py",                    N,       N,      N,      N,      N,     N,     N),
       ("15-rq-dq.py",                   Y,       N,      N,      N,      Y,     N,     N),
       ("15-rq-dq-bm1688-bm1690.py",     N,       N,      N,      N,      N,     N,     N),
       ("16-multicore.py",               N,       N,      Y,      N,      Y,     N,     N),
       ("17-uint.py",                    Y,       Y,      Y,      N,      N,     N,     N),
       ("19_autotiling.py",              N,       N,      Y,      N,      N,     N,     N),],
}
