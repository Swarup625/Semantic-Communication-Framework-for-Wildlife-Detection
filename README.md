# Semantic Communication Framework for Wildlife Detection

## Overview

This repository presents an experimental **Semantic Communication Framework for Wildlife Detection**, developed using computer vision and semantic information processing techniques.

The framework combines **YOLO-based object detection** and **MobileSAM-based segmentation** to identify wildlife objects and extract meaningful semantic information from captured images.

Unlike conventional image transmission systems, where the complete image is transmitted, the proposed framework focuses on transmitting information that is semantically relevant to the communication task.

The system processes wildlife images, detects relevant objects, extracts regions of interest, generates semantic metadata, prioritizes information, and prepares the resulting semantic data for transmission.

---

## Motivation

In conventional communication systems, the objective is to transmit raw data as accurately as possible.

However, in wildlife monitoring and IoT-based sensing systems, transmitting complete high-resolution images can consume significant:

- Bandwidth
- Energy
- Storage
- Communication time

In many cases, the receiver may only require meaningful information such as:

- Detected animal class
- Location of the animal
- Bounding box coordinates
- Confidence score
- Region of interest
- Segmented object information

Semantic communication aims to communicate the **meaningful information required by the receiver** rather than transmitting all raw source data.

This project explores this concept for intelligent wildlife monitoring.

---

# System Architecture

The overall framework follows the pipeline:

```text
                 Wildlife Image
                       │
                       ▼
              ┌─────────────────┐
              │      YOLO       │
              │ Object Detection│
              └────────┬────────┘
                       │
             Detected Object / ROI
                       │
                       ▼
              ┌─────────────────┐
              │    MobileSAM    │
              │ Object Segmentation
              └────────┬────────┘
                       │
                Segmented Object
                       │
                       ▼
              ┌─────────────────┐
              │ Semantic Metadata│
              │    Extraction    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Priority / ROI   │
              │    Processing    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Semantic Event   │
              │    Generation    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Packet Creation  │
              │ & Chunk Generation
              └────────┬────────┘
                       │
                       ▼
                 Communication
