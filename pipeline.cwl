#!/usr/bin/env cwl-runner
class: Workflow
cwlVersion: v1.1
requirements:
  ScatterFeatureRequirement: {}

inputs:
  ometiff_directory:
    type: Directory
  processes:
    type: int
    default: 1
  rgb:
    type: boolean?

outputs:
  pyramid_file:
    type: File[]
    outputSource: convert_to_pyramid/pyramid_file

steps:
  collect_ometiff_files:
    run: collect-ometiff-files.cwl
    in:
      ometiff_directory: ometiff_directory
    out:
      [ometiff_file]

  convert_to_pyramid:
    scatter: [ometiff_file]
    scatterMethod: dotproduct
    run: steps/ometiff-to-pyramid.cwl
    in:
      ometiff_file: collect_ometiff_files/ometiff_file
      processes: processes
      rgb: rgb
    out: [pyramid_file]
