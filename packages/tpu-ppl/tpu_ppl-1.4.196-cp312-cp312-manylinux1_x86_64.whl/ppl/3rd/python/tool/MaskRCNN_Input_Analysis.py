import numpy as np
import torch


input_all = np.load("/workspace/tpu-mlir/python/test/test_case_tpu_mlir_maskrcnn/test_case/get_bbox_B_input_all_real.npz")
for i in input_all.files:
  print(i, input_all[i].shape)

tag = "MaskRCNNGetBboxB"
batch_size =  input_all[input_all.files[0]].shape[0]
path_store_rois = "/workspace/ppl/data_MaskRCNN/input_tag_{}_rois_batch_{}.dat".format(tag, batch_size)
path_store_cls_score = "/workspace/ppl/data_MaskRCNN/input_tag_{}_cls_score_batch_{}.dat".format(tag, batch_size)
path_store_bbox_pred = "/workspace/ppl/data_MaskRCNN/input_tag_{}_bbox_pred_batch_{}.dat".format(tag, batch_size)
path_store_max_shape = "/workspace/ppl/data_MaskRCNN/input_tag_{}_max_shape_batch_{}.dat".format(tag, batch_size)
path_store_scale_factor = "/workspace/ppl/data_MaskRCNN/input_tag_{}_scale_factor_batch_{}.dat".format(tag, batch_size)

def save_dat(save_path, npz_input_all, i, given_input_target=None,given_i=None):
    if given_input_target is None:
      input_target = npz_input_all[npz_input_all.files[i]]
    else:
      assert i==-1
      assert given_i is not None, "[Error]you must give the real idx-input!"
      input_target = given_input_target
    input_target = input_target.astype(np.float32)
    input_target = np.ascontiguousarray(input_target)
    f = open(save_path, 'wb')
    f.write(input_target)
    f.close()
    new_i = i if given_i is None else  given_i
    check_dat(save_path, input_target,npz_input_all, new_i)

def check_dat(save_path, input_ref, npz_input_all, i):
    input_get = np.fromfile( \
       save_path, \
       dtype=np.float32)
    assert np.sum(np.abs(input_get-input_ref.flatten()))<1e-6
    print("[CMP] {} correctly stored at {} ".format(npz_input_all.files[i],save_path))

save_dat(path_store_rois,      input_all, 0)
save_dat(path_store_cls_score, input_all, 1)
save_dat(path_store_bbox_pred, input_all, 2)


real_input_idx = 5
raw_max_shape_data  = input_all[input_all.files[real_input_idx]]
raw_max_shape_data = torch.tensor(raw_max_shape_data)[:,:2]
A1=raw_max_shape_data[:,1].reshape([-1,1])
A2=raw_max_shape_data[:,0].reshape([-1,1])
new_max_shape_data = torch.concatenate([A1, A2,A1,A2],axis=1).reshape([1,4,1,4]).repeat([1,1,80000,1]).numpy()
save_dat(path_store_max_shape, input_all, -1,new_max_shape_data ,real_input_idx)


raw_scale_factor_data = input_all[input_all.files[6]]
new_scale_factor   = torch.tensor(raw_scale_factor_data).reshape(1,4,1,4).repeat([1,1,80000,1]).numpy()
save_dat(path_store_scale_factor, input_all, -1,new_scale_factor ,6)
#################################
#python3 /workspace/ppl/python/tools/MaskRCNN_Input_Analysis.py
