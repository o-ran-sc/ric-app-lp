# ==================================================================================
#       Copyright (c) 2018-2020 China Mobile Technology (USA) Inc. Intellectual Property.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ==================================================================================
FROM python:3.8-alpine

# RMR setup
RUN mkdir -p /opt/route/
# copy rmr files from builder image in lieu of an Alpine package
COPY --from=nexus3.o-ran-sc.org:10002/o-ran-sc/bldr-alpine3-rmr:4.0.5 /usr/local/lib64/librmr* /usr/local/lib64/
# rmr_probe replaced health_ck
COPY --from=nexus3.o-ran-sc.org:10002/o-ran-sc/bldr-alpine3-rmr:4.0.5 /usr/local/bin/rmr* /usr/local/bin/
ENV LD_LIBRARY_PATH /usr/local/lib/:/usr/local/lib64

# sdl needs gcc
RUN apk update && apk add gcc musl-dev g++ jpeg-dev zlib-dev

# Install
COPY setup.py /tmp
COPY LICENSE.txt /tmp/
COPY lp /tmp/lp
RUN pip install --upgrade pip setuptools wheel
RUN pip install /tmp
RUN pip install p5py
RUN pip install PEP517
RUN pip install Cython pandas 
RUN pip install --upgrade Pillow
RUN pip install torch==1.9.0+cpu torchvision==0.10.0+cpu torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html

# TO DO: ADD RUN COMMANDS 
ENV PYTHONUNBUFFERED 1
CMD start-lp.py
