CUDA_VISIBLE_DEVICES=0 python scripts/rgb2ir_vqf8.py --steps 200 \
--indir /root/autodl-tmp/PID/PID/dataset/crack/data4_split/train \
--outdir crack_test \
--config configs/latent-diffusion/kaist512-vqf8.yaml \
--checkpoint /root/autodl-tmp/PID/PID/pretrained/vqf8_pretrained/model.ckpt