#!/usr/bin/env cwl-runner
cwlVersion: v1.1
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: hubmap/ome-tiff-pyramid:latest

inputs:
  ometiff_file:
    type: File
    inputBinding:
      position: 0
  processes:
    type: int
    inputBinding:
      position: 1
  rgb:
    type: boolean?
    default: false
    inputBinding:
      prefix: --rgb
      position: 2

outputs:
  pyramid_file:
    type: File
    outputBinding:
      glob: '*.ome.tif'

baseCommand: ['python3', '/opt/ometiff_to_pyramid.py']
