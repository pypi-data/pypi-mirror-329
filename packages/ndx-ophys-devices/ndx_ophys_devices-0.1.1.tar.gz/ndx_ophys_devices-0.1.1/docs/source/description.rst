Overview
========

ndx-ophys-devices Extension for NWB
-----------------------------------

This is an NWB extension for storing metadata of devices used in optical experimental setups (microscopy, fiber photometry, optogenetic stimulation, etc.).

This extension consists of 11 new neurodata types:

- **DeviceModel** extends ``Device`` to hold metadata on the model of the device.
- **Indicator** extends ``NWBContainer`` to hold metadata on the fluorescent indicator (e.g., label=GCaMP6).
- **Effector** extends ``NWBContainer`` to hold metadata on the effector/opsin (e.g., label=hChR2).
- **OpticalFiber** extends ``DeviceModel`` to hold metadata on the optical fiber (e.g., numerical_aperture=0.39).
- **ExcitationSource** extends ``DeviceModel`` to hold metadata on the excitation source (e.g., excitation_wavelength_in_nm=470.0).
- **PulsedExcitationSource** extends ``ExcitationSource`` to hold metadata on the pulsed excitation source (e.g., pulse_rate_in_Hz=1000.0).
- **Photodetector** extends ``DeviceModel`` to hold metadata on the photodetector (e.g., detected_wavelength_in_nm=520.0).
- **DichroicMirror** extends ``DeviceModel`` to hold metadata on the dichroic mirror (e.g., cut_on_wavelength_in_nm=470.0).
- **OpticalFilter** extends ``DeviceModel`` to hold metadata on a general optical filter (e.g., filter_type='Bandpass').
- **BandOpticalFilter** extends ``OpticalFilter`` to hold metadata on any bandpass or bandstop optical filters (e.g., center_wavelength_in_nm=505.0).
- **EdgeOpticalFilter** extends ``OpticalFilter`` to hold metadata on any edge optical filters (e.g., cut_wavelength_in_nm=585.0).
- **ObjectiveLens** extends ``DeviceModel`` to hold metadata on the objective lens (e.g., magnification=60.0).

Installation
------------

To install the latest stable release through PyPI, run:

.. code-block:: bash

    pip install ndx-ophys-devices

Usage
-----

.. code-block:: python

    import datetime
    import numpy as np
    from pynwb import NWBFile
    from ndx_ophys_devices import (
        Indicator,
        OpticalFiber,
        ExcitationSource,
        PulsedExcitationSource,
        Photodetector,
        DichroicMirror,
        BandOpticalFilter,
        EdgeOpticalFilter,
        ObjectiveLens,
        Effector,
    )

    nwbfile = NWBFile(
        session_description='session_description',
        identifier='identifier',
        session_start_time=datetime.datetime.now(datetime.timezone.utc)
    )

    indicator = Indicator(
        name="indicator",
        description="Green indicator",
        label="GCamp6f",
        injection_brain_region="VTA",
        injection_coordinates_in_mm=(3.0, 2.0, 1.0),
    )
    effector = Effector(
        name="effector",
        description="Excitatory opsin",
        label="hChR2",
        injection_brain_region="VTA",
        injection_coordinates_in_mm=(3.0, 2.0, 1.0),
    )

    optical_fiber = OpticalFiber(
        name="optical_fiber",
        manufacturer="fiber manufacturer",
        model="fiber model",
        numerical_aperture=0.2,
        core_diameter_in_um=400.0,
    )

    objective_lens = ObjectiveLens(
        name="objective_lens",
        manufacturer="objective lens manufacturer",
        model="objective lens model",
        numerical_aperture=0.39,
        magnification=40.0,
    )

    excitation_source = ExcitationSource(
        name="excitation_source",
        description="excitation sources for green indicator",
        manufacturer="laser manufacturer",
        model="laser model",
        illumination_type="laser",
        excitation_mode="one-photon",
        excitation_wavelength_in_nm=470.0,
        power_in_W= 0.7,
        intensity_in_W_per_m2= 0.005,
    )
    pulsed_excitation_source = PulsedExcitationSource(
        name="pulsed_excitation_source",
        description="pulsed excitation sources for red indicator",
        manufacturer="laser manufacturer",
        model="laser model",
        illumination_type="laser",
        excitation_mode="two-photon",
        excitation_wavelength_in_nm=525.0,
        peak_power_in_W=0.7,
        peak_pulse_energy_in_J=0.7,
        intensity_in_W_per_m2=0.005,
        exposure_time_in_s=2.51e-13,
        pulse_rate_in_Hz=2.0e6,
    )

    photodetector = Photodetector(
        name="photodetector",
        description="photodetector for green emission",
        manufacturer="photodetector manufacturer",
        model="photodetector model",
        detector_type="PMT",
        detected_wavelength_in_nm=520.0,
        gain=100.0,
    )

    dichroic_mirror = DichroicMirror(
        name="dichroic_mirror",
        description="Dichroic mirror for green indicator",
        manufacturer="dichroic mirror manufacturer",
        model="dichroic mirror model",
        cut_on_wavelength_in_nm=470.0,
        transmission_band_in_nm=(460.0, 480.0),
        cut_off_wavelength_in_nm=500.0,
        reflection_band_in_nm=(490.0, 520.0),
        angle_of_incidence_in_degrees=45.0,
    )

    band_optical_filter = BandOpticalFilter(
        name="band_optical_filter",
        description="excitation filter for green indicator",
        manufacturer="filter manufacturer",
        model="filter model",
        center_wavelength_in_nm=480.0,
        bandwidth_in_nm=30.0, # 480±15nm
        filter_type="Bandpass",
    )

    edge_optical_filter = EdgeOpticalFilter(
        name="edge_optical_filter",
        description="emission filter for green indicator",
        model="emission filter model",
        cut_wavelength_in_nm=585.0,
        slope_in_percent_cut_wavelength=1.0,
        slope_starting_transmission_in_percent=10.0,
        slope_ending_transmission_in_percent=80.0,
        filter_type="Longpass",
    )

    nwbfile.add_lab_metadata(indicator)
    nwbfile.add_lab_metadata(effector)
    nwbfile.add_device(optical_fiber)
    nwbfile.add_device(objective_lens)
    nwbfile.add_device(excitation_source)
    nwbfile.add_device(pulsed_excitation_source)
    nwbfile.add_device(photodetector)
    nwbfile.add_device(dichroic_mirror)
    nwbfile.add_device(band_optical_filter)
    nwbfile.add_device(edge_optical_filter)


