"""Test in-memory Python API constructors for ndx-ophys-devices extension."""

import pytest

from ndx_ophys_devices.testing import (
    mock_DeviceModel,
    mock_Indicator,
    mock_Effector,
    mock_OpticalFiber,
    mock_Photodetector,
    mock_DichroicMirror,
    mock_OpticalFilter,
    mock_BandOpticalFilter,
    mock_EdgeOpticalFilter,
    mock_ObjectiveLens,
    mock_ExcitationSource,
    mock_PulsedExcitationSource,
)


def test_constructor_device_model():
    mock_DeviceModel()


def test_constructor_indicator():
    mock_Indicator()


def test_constructor_effector():
    mock_Effector()


def test_constructor_optical_fiber():
    mock_OpticalFiber()


def test_constructor_photodetector():
    mock_Photodetector()


def test_constructor_dichroic_mirror():
    mock_DichroicMirror()


def test_constructor_optical_filter():
    mock_OpticalFilter()


def test_constructor_band_optical_filter():
    mock_BandOpticalFilter()


def test_constructor_edge_optical_filter():
    mock_EdgeOpticalFilter()


def test_constructor_objective_lens():
    mock_ObjectiveLens()


def test_constructor_excitation_source():
    mock_ExcitationSource()


def test_constructor_excitation_source_with_wrong_mode():
    excitation_mode = "1P"
    expected_error_message = (
        f"excitation_mode must be one of 'one-photon', 'two-photon', "
        f"'three-photon', 'other', not {excitation_mode}. "
        f"If you want to include a different excitation mode, please open an issue on GitHub at "
        f"https://github.com/CatalystNeuro/ndx-microscopy/issues"
    )
    with pytest.raises(ValueError, match=expected_error_message):
        _ = mock_ExcitationSource(excitation_mode=excitation_mode)


def test_constructor_pulsed_excitation_source():
    mock_PulsedExcitationSource()


def test_constructor_pulsed_excitation_source_with_wrong_mode():
    excitation_mode = "1P"
    expected_error_message = (
        f"excitation_mode must be one of 'one-photon', 'two-photon', "
        f"'three-photon', 'other', not {excitation_mode}. "
        f"If you want to include a different excitation mode, please open an issue on GitHub at "
        f"https://github.com/CatalystNeuro/ndx-microscopy/issues"
    )
    with pytest.raises(ValueError, match=expected_error_message):
        _ = mock_PulsedExcitationSource(excitation_mode=excitation_mode)


if __name__ == "__main__":
    pytest.main()  # Required since not a typical package structure
