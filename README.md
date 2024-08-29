# Quick start
## 1. Conda environment
```
conda create python=3.10 --name render
conda activate render
```
Install the packages in `requirements.txt` and install [PyTorch 2.0](https://pytorch.org/)
```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```
## 2. get smpl model
Download from [Google Drive](https://drive.google.com/file/d/19tPn-QH6_p5jwkvEKjy5t06Hoq_ZRVNb/view?usp=share_link) and place it to `./body_models`
## 3. Set up blender
Download from [Google Drive](https://drive.google.com/file/d/1DqcCfyBgqu9r7xkupi8x-CElvyJgOXCI/view?usp=share_link) and place it to `path/to/YOUR_BLENDER_PATH`
## 4. Render one npy file
```
YOUR_BLENDER_PATH/blender --background --python render2video.py -- --cfg=./configs/render.yaml --npy=YOUR_NPY_File --mode=video
```
Where `YOUR_NPY_FOLDER` is the joints data, for example, `path/to/HumanML3D/new_joints/000000.npy' 


You can add `--mesh=True` to render smpl meshes.
## 4. Render SMPL meshes
```
YOUR_BLENDER_PATH/blender --background --python render2video.py -- --cfg=./configs/render.yaml --dir=YOUR_NPY_FOLDER --mode=video --mesh=True
```
Where `YOUR_NPY_FOLDER` place the joints data, for example,  `path/to/HumanML3D/new_joints`
## 4. Render joints
```
YOUR_BLENDER_PATH/blender --background --python render2video.py -- --cfg=./configs/render.yaml --dir=YOUR_NPY_FOLDER --mode=video
```
Where `YOUR_NPY_FOLDER` place the joints data, for example, `path/to/HumanML3D/new_joints' 
