from abc import ABC, abstractmethod
import numpy as np
from .directory_manager import DirectoryManager
from .utils import write_to_csv, format_array

class BaseOptimiser(ABC):
	"""
	Base class for optimisers, providing a common interface and functionality.
	"""
	def __init__(
		self,
		parameters: dict,
		evaluator,
		batch_size: int,
		directory_manager: DirectoryManager,
		sigma_threshold: float = 0.1,
		rand_seed: int = 1,
		start_epoch: int = None,
		verbose: bool = False,
		n_epochs: int = None,
	):
		"""
		Initialise the BaseOptimiser.

		Args:
			parameters (dict): A dictionary defining the parameters to optimise,
				where keys are parameter names and values are tuples of (min, max) bounds.
			evaluator: A callable that evaluates the parameters and returns an error value.
			batch_size (int): The number of solutions to evaluate in each epoch.
			directory_manager (DirectoryManager): An instance of the DirectoryManager
				to handle file and directory operations.
			sigma_threshold (float, optional): Threshold for sigma values to terminate optimisation. Defaults to 0.01.
			rand_seed (int, optional): Random seed for reproducibility. Defaults to 1.
			start_epoch (int, optional): Epoch to start from (for resuming). Defaults to None.
			verbose (bool, optional): Whether to print detailed information during optimisation. Defaults to False.
			n_epochs (int, optional): The number of epochs to run the optimisation for. If None, the optimisation runs until the termination criteria is met. Defaults to None.
		"""
		self.parameters = parameters
		self.evaluator = evaluator
		self.n_epochs = n_epochs
		self.batch_size = batch_size
		self.dir_manager = directory_manager
		self.sigma_threshold = sigma_threshold
		self.rand_seed = rand_seed
		self.start_epoch = start_epoch
		self.verbose = verbose
		self.current_epoch = 0 # Previously None
		np.random.seed(rand_seed)
		self.init_sigmas = self.get_init_sigmas
		self.norm_bounds = self.get_norm_bounds
		self.init_params = self.get_init_params
		

	@property
	def get_init_sigmas(self):
		"""
		Calculate initial standard deviation values based on parameter bounds.

		Returns:
			np.ndarray: An array of initial standard deviation values for each parameter.
		"""
		return np.array([(max_val - min_val) / 4 for min_val, max_val in self.parameters.values()])

	@property
	def get_norm_bounds(self):
		"""
		Calculate bounds for the parameters normalised by the initial standard deviations.

		Returns:
			list: A list of tuples containing the normalised min and max bounds for each parameter.
		"""
		return [(min_val / std, max_val / std)
				for (min_val, max_val), std in zip(self.parameters.values(), self.init_sigmas)]

	@property
	def get_init_params(self):
		"""
		Generate initial parameters uniformly within the normalised bounds.

		Returns:
			list: A list of initial parameter values.
		"""
		# Generate initial parameters uniformly in the normalised bounds
		return [np.random.uniform(low, high) for low, high in self.norm_bounds]
	
	def rescale_params(self, params):
		"""
		Rescale normalised parameters to their original scale.

		Args:
			params (np.ndarray): Normalised parameter values.

		Returns:
			np.ndarray: Rescaled parameter values.
		"""
		return params * self.init_sigmas


	def _write_result_to_csv(self, sol, error, param_dict):
		"""
		Write the results of a solution to a CSV file.
		The CSV file is structured as:
		 | Epoch | Solution | Error | Param1 | Param2 | ... | ParamN |

		Args:
			sol (int): The solution number.
			error (float): The error value for the solution.
			param_dict (dict): A dictionary of parameter values for the solution.
		"""
		result = {
			'epoch': self.current_epoch,
			'solution': sol,
			'error': error,
			**param_dict
			}
		write_to_csv(result, self.dir_manager.results_csv)

	def _write_epoch_to_csv(self, mean_error, sigma_error, mean_params, sigma_params, norm_sigmas):
		"""
		Write epoch data to a CSV file.
		The CSV file is structured as:
		 | Epoch | Mean Error | Mean ParamN | Sigma Error | Sigma ParamN | Norm SigmaN |

		Args:
			mean_error (float): The mean error for the epoch.
			sigma_error (float): The standard deviation of the errors for the epoch.
			mean_params (np.ndarray): The mean parameter values for the epoch.
			sigma_params (np.ndarray): The standard deviation of the parameter values for the epoch.
			norm_sigmas (np.ndarray): The normalised sigma values for the parameters.
		"""
		epoch_data = {
			'Epoch': self.current_epoch,
			'Mean error': mean_error,
			**{f"Mean {param}": mean for param, mean in zip(self.parameters.keys(), mean_params)},
			'Sigma error': sigma_error,
			**{f"Sigma {param}": sigma for param, sigma in zip(self.parameters.keys(), sigma_params)},
			**{f"Norm sigma {param}": norm_sigma for param, norm_sigma in zip(self.parameters.keys(), norm_sigmas)}
		}
		write_to_csv(epoch_data, self.dir_manager.epochs_csv)

	def print_solution(self, sol_id, params, error):
		"""
		Print the results of a solution to terminal and log.

		Args:
			sol_id (int): The solution ID.
			params (np.ndarray): The parameter values for the solution.
			error (float): The error value for the solution.
		"""
		print(f"Epoch {self.current_epoch} | ({sol_id + 1}/{self.batch_size}) | Params: [{format_array(params)}] | Error: {error:.3f}")

	def print_epoch(self, mean_error, sigma_error, mean_params, sigma_params, norm_sigmas):
		"""
		Print the epoch statistics to terminal and log

		Args:
			mean_error (float): The mean error for the epoch.
			sigma_error (float): The standard deviation of the errors for the epoch.
			mean_params (np.ndarray): The mean parameter values for the epoch.
			sigma_params (np.ndarray): The standard deviation of the parameter values for the epoch.
			norm_sigmas (np.ndarray): The normalised sigma values for the parameters.
		"""
		print(f"Epoch {self.current_epoch} | Mean Error: {mean_error:.3f} | Sigma Error: {sigma_error:.3f}")
		print(f"Epoch {self.current_epoch} | Mean Parameters: [{format_array(mean_params)}] | Sigma parameters: [{format_array(sigma_params)}]")
		print(f"Epoch {self.current_epoch} | Normalised Sigma parameters: [{format_array(norm_sigmas)}]")

	def process_batch(self, solutions):
		"""
		Process a batch of solutions, evaluate them, and write the results to CSV.

		Args:
			solutions (list): A list of parameter value arrays.

		Returns:
			list: A list of error values for each solution.
		"""
		# in series, future work to parallelise
		errors = []
		for sol, params in enumerate(solutions):
			rescaled = self.rescale_params(params)
			param_dict = dict(zip(self.parameters.keys(), rescaled))
			solution_folder = self.dir_manager.create_solution_folder(self.current_epoch, sol)
			with self.dir_manager.working_directory(solution_folder):
				error = self.evaluator(param_dict)

			self.print_solution(sol, rescaled, error)
			self._write_result_to_csv(sol, error, param_dict)
			errors.append(error)

		valid_err = [err for err in errors if err is not None]
		if not valid_err:
			raise ValueError("All errors are None")
		errors = [err if err is not None else float(np.mean(valid_err)) for err in errors]

		rescaled_solutions = [self.rescale_params(sol) for sol in solutions]
		mean_error = np.mean(errors)
		sigma_error = np.std(errors)
		mean_params = np.mean(rescaled_solutions, axis=0)
		sigma_params = np.std(rescaled_solutions, axis=0)
		norm_sigmas = sigma_params / self.init_sigmas

		self.print_epoch(mean_error, sigma_error, mean_params, sigma_params, norm_sigmas)
		self._write_epoch_to_csv(mean_error, sigma_error, mean_params, sigma_params, norm_sigmas)
		return errors


	@abstractmethod
	def setup_opt(self, epoch=None):
		"""
		Abstract method to set up the optimiser. Must be implemented by subclasses.

		Args:
			epoch (int, optional): The epoch number to start from. Defaults to None.
		"""
		pass

	@abstractmethod
	def check_termination(self):
		"""
		Abstract method to check termination criteria. Must be implemented by subclasses.

		Returns:
			bool: True if the termination criteria are met, False otherwise.
		"""
		pass

	@abstractmethod
	def optimise(self):
		"""
		Abstract method to run the optimisation. Must be implemented by subclasses.
		"""
		pass
