from collections import OrderedDict

extension_to_point_set_io = OrderedDict([
    ('.mz3', 'mz3'),
    ('.vtk', 'vtk_poly_data'),
    ('.obj', 'obj'),
    ('.off', 'off'),
    ('.iwm', 'wasm'),
    ('.iwm.cbor', 'wasm'),
    ('.iwm.cbor.zst', 'wasm_zstd'),
])
