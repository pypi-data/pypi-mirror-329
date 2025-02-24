from setuptools import setup, find_packages


 
setup(
    
  name='OwlSense',
  version='0.7',
  description='Python lib for basic&advance AI,ML',
  author='sebinmon.vr',
  author_email='nthn8777@gmail.com',
  license='MIT', 
  packages=find_packages(),
  install_requires=['openai==0.28'] ,
  entry_points = {
    'console_scripts': ['OwlSense=OwlSense.main:Owl'],
  },
  
)

