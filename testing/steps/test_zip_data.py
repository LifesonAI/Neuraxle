import numpy as np

from neuraxle.base import ExecutionContext
from neuraxle.data_container import DataContainer
from neuraxle.pipeline import Pipeline
from neuraxle.steps.data import ZipData

TIMESTEPS = 10
FEATURES = 5
VALIDATION_SIZE = 0.1
BATCH_SIZE = 32
N_EPOCHS = 10
SHAPE_3D = (BATCH_SIZE, TIMESTEPS, FEATURES)
SHAPE_2D = (BATCH_SIZE, TIMESTEPS)
SHAPE_1D = BATCH_SIZE


def test_zip_data_should_merge_2d_with_3d():
    # Given
    data_inputs_3d, expected_outputs_3d = _create_data_source(SHAPE_3D)
    data_inputs_2d, expected_outputs_2d = _create_data_source(SHAPE_2D)
    data_container_2d = DataContainer(data_inputs=data_inputs_2d, expected_outputs=expected_outputs_2d)
    data_container_3d = DataContainer(data_inputs=data_inputs_3d, expected_outputs=expected_outputs_3d) \
        .add_sub_data_container('2d', data_container_2d)

    # When
    p = Pipeline([
        ZipData(data_sources=['2d'])
    ])

    data_container_3d = p.handle_transform(data_container_3d, ExecutionContext())

    # Then
    assert data_container_3d.data_inputs.shape == (SHAPE_3D[0], SHAPE_3D[1], SHAPE_3D[2] + 1)
    assert data_container_3d.expected_outputs.shape == (SHAPE_3D[0], SHAPE_3D[1], SHAPE_3D[2] + 1)
    assert np.array_equal(data_container_3d.data_inputs[..., -1], data_container_2d.data_inputs)
    assert np.array_equal(data_container_3d.expected_outputs[..., -1], data_container_2d.expected_outputs)


def test_zip_data_should_merge_1d_with_3d():
    # Given
    data_inputs_3d, expected_outputs_3d = _create_data_source(SHAPE_3D)
    data_inputs_1d, expected_outputs_1d = _create_data_source(SHAPE_1D)
    data_container_1d = DataContainer(data_inputs=data_inputs_1d, expected_outputs=expected_outputs_1d)
    data_container = DataContainer(data_inputs=data_inputs_3d, expected_outputs=expected_outputs_3d) \
        .add_sub_data_container('1d', data_container_1d)

    # When
    p = Pipeline([
        ZipData(data_sources=['1d'])
    ])

    data_container = p.handle_transform(data_container, ExecutionContext())

    # Then
    assert data_container.data_inputs.shape == (SHAPE_3D[0], SHAPE_3D[1], SHAPE_3D[2] + 1)
    assert data_container.expected_outputs.shape == (SHAPE_3D[0], SHAPE_3D[1], SHAPE_3D[2] + 1)
    assert np.array_equal(data_container.data_inputs[..., -1], data_container_1d.data_inputs)
    assert np.array_equal(data_container.expected_outputs[..., -1], data_container_1d.expected_outputs)


def test_zip_data_should_merge_1d_with_2d():
    # Given
    data_inputs_2d, expected_outputs_2d = _create_data_source(SHAPE_2D)
    data_inputs_1d, expected_outputs_1d = _create_data_source(SHAPE_1D)
    data_container_1d = DataContainer(data_inputs=data_inputs_1d, expected_outputs=expected_outputs_1d)
    data_container = DataContainer(data_inputs=data_inputs_2d, expected_outputs=expected_outputs_2d) \
        .add_sub_data_container('1d', data_container_1d)

    # When
    p = Pipeline([
        ZipData(data_sources=['1d'])
    ])

    data_container = p.handle_transform(data_container, ExecutionContext())

    # Then
    assert data_container.data_inputs.shape == (SHAPE_2D[0], SHAPE_2D[1] + 1)
    assert data_container.expected_outputs.shape == (SHAPE_2D[0], SHAPE_2D[1] + 1)
    assert np.array_equal(data_container.data_inputs[..., -1], data_container_1d.data_inputs * SHAPE_2D[1])
    assert np.array_equal(data_container.expected_outputs[..., -1], data_container_1d.expected_outputs * SHAPE_2D[1])


def _create_data_source(shape):
    data_inputs = np.random.random(shape).astype(np.float32)
    expected_outputs = np.random.random(shape).astype(np.float32)
    return data_inputs, expected_outputs
