// -*- c++ -*-

#include <cuComplex.h>
#include <cuda.h>
#include <cuda_fp16.h>
#include <cuda_runtime.h>
#include <stdexcept>
#include <stdio.h>

#ifndef KSMM
#define KSMM

#if defined(V1)
#define VSIZE 1
#elif defined(V2)
#define VSIZE 2
#elif defined(V3)
#define VSIZE 3
#elif defined(V4)
#define VSIZE 4
#endif

#ifdef USE_FLOAT16
#define SUPPORT_FLOAT16
#endif

#ifdef USE_FLOAT32
#define SUPPORT_FLOAT32
#endif

#ifdef USE_COMPLEX64
#define SUPPORT_COMPLEX64
#define SUPPORT_COMPLEX
#endif

#ifdef USE_FLOAT64
#define SUPPORT_FLOAT64
#endif

#ifdef USE_COMPLEX128
#define SUPPORT_COMPLEX128
#define SUPPORT_COMPLEX
#endif

#ifdef SUPPORT_FLOAT16
typedef __half real_t;
#if defined(V1)
typedef __half realx_t;
#endif
#if defined(V2)
typedef __half2 realx_t;
#endif
#if defined(V3)
typedef half3 realx_t;
#endif
#if defined(V4)
typedef half4 realx_t;
#endif
#endif

#ifdef SUPPORT_FLOAT32
typedef float real_t;
#if defined(V1)
typedef float realx_t;
#endif
#if defined(V2)
typedef float2 realx_t;
#endif
#if defined(V3)
typedef float3 realx_t;
#endif
#if defined(V4)
typedef float4 realx_t;
#endif
#endif

#ifdef SUPPORT_FLOAT64
typedef double real_t;
#if defined(V1)
typedef double realx_t;
#endif
#if defined(V2)
typedef double2 realx_t;
#endif
#if defined(V3)
typedef double3 realx_t;
#endif
#if defined(V4)
typedef double4 realx_t;
#endif
#endif

#ifdef SUPPORT_COMPLEX64
typedef cuFloatComplex real_t;
typedef cuFloatComplex realx_t;
#endif

#ifdef SUPPORT_COMPLEX128
typedef cuDoubleComplex real_t;
typedef cuDoubleComplex realx_t;
#endif

#define loadx(a, b)                                                            \
  reinterpret_cast<realx_t *>(&a)[0] = reinterpret_cast<realx_t *>(&b)[0]

__device__ inline void kload(real_t *gmem, real_t *smem, int c, int row, int s,
                             int col, realx_t src) {
#if defined(SUPPORT_COMPLEX64) || defined(SUPPORT_COMPLEX128)
  for (int v = 0; v < VSIZE; v++)
    smem[(col * VSIZE + v) * xTILEYx + row + s] = gmem[v];
#else
#if defined(V1)
 smem[col * VSIZE * xTILEYx + row + s] = gmem[0];
#else
  loadx(src, gmem[0]);
  smem[(col * VSIZE + 0) * xTILEYx + row + s] = src.x;
  smem[(col * VSIZE + 1) * xTILEYx + row + s] = src.y;
#if defined(V3)
  smem[(col * VSIZE + 2) * xTILEYx + row + s] = src.z;
#elif defined(V4)
  smem[(col * VSIZE + 2) * xTILEYx + row + s] = src.z;
  smem[(col * VSIZE + 3) * xTILEYx + row + s] = src.w;
#endif
#endif
#endif
}

__device__ inline void iload(real_t *gmem, real_t *smem, int batch_size,
                             int row, int s, int col, int offset) {
#if defined(SUPPORT_COMPLEX64) || defined(SUPPORT_COMPLEX128)
  for (int v = 0; v < VSIZE; v++)
    smem[(row + s) * xTILEXx + col * VSIZE + v] = gmem[v];
#else
#if defined(V1)
  smem[(row + s) * xTILEXx + col * VSIZE] = gmem[0];
#else
  offset += col * VSIZE;
  if ((batch_size - offset) >= VSIZE) {
    loadx(smem[(row + s) * xTILEXx + col * VSIZE], gmem[0]);
  } else {
    for (int v = 0; v < (batch_size - offset); v++)
      smem[(row + s) * xTILEXx + col * VSIZE + v] = gmem[v];
  }
#endif
#endif
}

extern "C" {
__global__ void ksmm(real_t *values, real_t *input, real_t *output, const int a,
                     const int b, const int c, const int d, int batch_size) {
  int bx = blockIdx.x;
  int by = blockIdx.y;
  int t_id = threadIdx.x * blockDim.y + threadIdx.y;
  // Kronecker-sparse pattern (a, b, c, d)
  // K = kron(Id_{a,a}, kron(1_{b,c}, Id_{d,d}))
  // There is 'a' super-blocks of shape (b * d, c * d).
  // Number of non-zero per super-block is
  // b per column and c per row.
  // We would like to compute K @ X.
  // K (row-major format) shape is (a * b * d, a * c * d).
  // X (row-major format) shape is (a * c * d, batch).
  // TILEX / TX threads per column
  // Get the current thread
  int threadx = t_id % (xTILEXx / xTXx);
  int thready = t_id / (xTILEXx / xTXx);
  // To store input in shared memory
  __shared__ real_t shared_input[2][xTILEKx * xTILEXx];
  // To store sparse matrix in shared memory
  __shared__ real_t shared_values[2][xTILEYx * xTILEKx];
  // To store output in shared memory
  __shared__ real_t shared_output[xTILEYx * xTILEXx];
  real_t tmp_acc[xTYx * xTXx] = {0.0};
  real_t regY[xTYx] = {0.0};
  real_t regX[xTXx] = {0.0};

  realx_t src;

  // Current super-block.
  int sb_id = (by * xTILEYx) / (b * d);
  // Group and id inside the super-block.
  int grp_id = (by * xTILEYx - sb_id * b * d) / b;
  int off = ((by * xTILEYx - sb_id * b * d) % b) / xTILEYx;
  // Move to the current super-block, group and id.
  values = &values[(sb_id * b * d + grp_id + off * d * xTILEYx) * c];
  input = &input[(c * d * sb_id + grp_id % d) * batch_size];
  output = &output[(sb_id * b * d + grp_id + off * d * xTILEYx) * batch_size];
  // Move bx * TILEX columns.
  input += bx * xTILEXx;
  output += bx * xTILEXx;

  // int diff;
  // int rem;

  // Indices to load (Kronecker-sparse factor) in smem.
  int ValuesSubRow = t_id / (xTILEKx / VSIZE);
  int ValuesSubCol = t_id % (xTILEKx / VSIZE);
  // Indices to load (input matrix) in smem.
  int InputSubRow = t_id / (xTILEXx / VSIZE);
  int InputSubCol = t_id % (xTILEXx / VSIZE);

  // Use stride to load from GMEM to SMEM
  const int StrideValues = VSIZE * xNTHREADSx / xTILEKx;
  const int StrideInput = VSIZE * xNTHREADSx / xTILEXx;

  // Load (realx_t) the first batch of Kronecker-sparse factor from global to
  // shared memory TILEY * TILEK.
#pragma unroll
  for (int s = 0; s < xTILEYx; s += StrideValues)
    kload(&values[d * (ValuesSubRow + s) * c + (ValuesSubCol * VSIZE) % c],
          &shared_values[0][0], c, ValuesSubRow, s, ValuesSubCol, src);

  // Load the first batch of input from global to shared memory TILEK * TILEX.
#pragma unroll
  for (int s = 0; s < xTILEKx; s += StrideInput)
    iload(&input[d * (InputSubRow + s) * batch_size + InputSubCol * VSIZE],
          &shared_input[0][0], batch_size, InputSubRow, s, InputSubCol,
          bx * xTILEXx);

  int load = 0;
  int write = 1;

  // Loop over non-zero entries by TILEK
  for (int k = 0; k < xTILEKx * (c / xTILEKx); k += xTILEKx) {
    __syncthreads();
    // Load smem to register and compute accumulation.
#pragma unroll
    for (int i = 0; i < xTILEKx; i++) {
      // Kronecker-sparse factor.
#pragma unroll
      for (int y = 0; y < xTYx; y += VSIZE) {
#ifdef SUPPORT_COMPLEX
        // No cuFloatComplexX and cuDoubleComplexX structs yet ?
        for (int v = 0; v < VSIZE; v++)
          regY[y + v] =
	    shared_values[load][i * xTILEYx + thready * xTYx + y + v];
#else
#if defined(V1)
	regY[y] = shared_values[load][i * xTILEYx + thready * xTYx + y];
#else
	loadx(regY[y], shared_values[load][i * xTILEYx + thready * xTYx + y]);
#endif
#endif
      }
      // Input.
#pragma unroll
      for (int x = 0; x < xTXx; x += VSIZE) {
#ifdef SUPPORT_COMPLEX
        // No cuFloatComplexX and cuDoubleComplexX structs yet ?
        for (int v = 0; v < VSIZE; v++)
          regX[x + v] =
	    shared_input[load][i * xTILEXx + threadx * xTXx + x + v];
#else
#if defined(V1)
        regX[x] = shared_input[load][i * xTILEXx + threadx * xTXx + x];
#else
        loadx(regX[x], shared_input[load][i * xTILEXx + threadx * xTXx + x]);
#endif
#endif
      }

      // Compute accumulation.
#pragma unroll
      for (int y = 0; y < xTYx; y++) {
#pragma unroll
        for (int x = 0; x < xTXx; x++) {
#if defined(SUPPORT_COMPLEX64)
          tmp_acc[y * xTXx + x] =
              cuCaddf(tmp_acc[y * xTXx + x], cuCmulf(regY[y], regX[x]));
#elif defined(SUPPORT_COMPLEX128)
          tmp_acc[y * xTXx + x] =
              cuCadd(tmp_acc[y * xTXx + x], cuCmul(regY[y], regX[x]));
#else
          tmp_acc[y * xTXx + x] += regY[y] * regX[x];
#endif
        }
      }
    }

    load = load ^ 1;
    // Move xTILEKx columns (values is in row-major).
    values += xTILEKx;
    // Move d * xTILEKx rows (input is in row-major).
    input += d * xTILEKx * batch_size;

    // Condition on columns of values.
    if ((k + xTILEKx) < (xTILEKx * (c / xTILEKx))) {
      // Load the Kronecker-sparse factor in shared memory TILEY x TILEK.
#pragma unroll
      for (int s = 0; s < xTILEYx; s += StrideValues)
        kload(&values[d * (ValuesSubRow + s) * c + (ValuesSubCol * VSIZE) % c],
              &shared_values[write][0], c, ValuesSubRow, s, ValuesSubCol, src);
        // Load next batch from global to shared memory TILEK x TILEX
#pragma unroll
      for (int s = 0; s < xTILEKx; s += StrideInput)
        iload(&input[d * (InputSubRow + s) * batch_size + InputSubCol * VSIZE],
              &shared_input[write][0], batch_size, InputSubRow, s, InputSubCol,
              bx * xTILEXx);
      write = write ^ 1;
    }
  }

  // Store accumulation to shared memory
#pragma unroll
  for (int y = 0; y < xTYx; y++) {
#pragma unroll
    for (int x = 0; x < xTXx; x += VSIZE) {
#ifdef SUPPORT_COMPLEX
      // No cuFloatComplexX and cuDoubleComplexX structs yet ?
#pragma unroll
      for (int v = 0; v < VSIZE; v++)
	shared_output[(thready * xTYx + y) * xTILEXx + threadx * xTXx + x + v] =
	  tmp_acc[y * xTXx + x + v];
#else
#if defined(V1)
      shared_output[(thready * xTYx + y) * xTILEXx + threadx * xTXx + x] =
	tmp_acc[y * xTXx + x];
#else
      loadx(shared_output[(thready * xTYx + y) * xTILEXx + threadx * xTXx + x],
	    tmp_acc[y * xTXx + x]);
#endif
#endif
    }
  }

  // Write out the accumulation (from shared to global memory).
//   diff = batch_size - (bx * xTILEXx + threadx * xTXx);
//   rem = diff >= xTXx ? xTXx : diff;
// #pragma unroll
//   for (int y = 0; y < xTYx; y++) {
// #pragma unroll
//     for (int x = 0; x < rem; x++)
//       output[threadx * xTXx + x + d * (thready * xTYx + y) * batch_size] =
//           shared_output[(thready * xTYx + y) * xTILEXx + threadx * xTXx + x];
//   }
#pragma unroll
  for (int y = 0; y < xTYx; y++) {
#pragma unroll
    for (int x = 0; x < xTXx; x += VSIZE) {
#ifdef SUPPORT_COMPLEX
#pragma unroll
      for (int v = 0; v < VSIZE; v++)
	output[d * (thready * xTYx + y) * batch_size + threadx * xTXx + x + v] =
	  shared_output[(thready * xTYx + y) * xTILEXx + threadx * xTXx + x + v];
#else
#if defined(V1)
      output[d * (thready * xTYx + y) * batch_size + threadx * xTXx + x] =
	shared_output[(thready * xTYx + y) * xTILEXx + threadx * xTXx + x];
#else
      loadx(output[d * (thready * xTYx + y) * batch_size + threadx * xTXx + x],
	    shared_output[(thready * xTYx + y) * xTILEXx + threadx * xTXx + x]);
#endif
#endif
    }
  }
}
}

#endif
