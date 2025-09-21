from rfdetr import RFDETRMedium

model = RFDETRMedium()

model.train(dataset_dir="/home/vira/rf-dter/dataset", epochs=300, batch_size=4, grad_accum_steps=1, lr=1e-4)
