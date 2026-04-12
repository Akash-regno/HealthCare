"""
Edge Impulse ECG Model Integration
This module provides edge-based ECG anomaly detection using Edge Impulse SDK
Designed for edge computing deployment at device level
"""

import numpy as np
import sys
from typing import Tuple, Dict, Any

class EdgeImpulseECGModel:
    """
    Edge Impulse Models for ECG-based anomaly detection
    Supports on-device inference with minimal resource footprint
    """
    
    def __init__(self, model_path: str = None, use_model: str = "edge"):
        """
        Initialize Edge Impulse ECG Model
        
        Args:
            model_path: Path to Edge Impulse model file or deployment
            use_model: 'edge' for edge-impulse-sdk, 'fallback' for local inference
        """
        self.use_model = use_model
        self.model_path = model_path
        self.model = None
        self.input_shape = None
        self.output_classes = ["Normal", "Abnormal"]
        
        try:
            if use_model == "edge":
                self._load_edge_impulse_model()
            else:
                print("⚠️  Using fallback inference mode (no Edge Impulse SDK)")
                self._setup_fallback_mode()
        except ImportError:
            print("⚠️  Edge Impulse SDK not found. Using fallback inference mode...")
            self._setup_fallback_mode()
        except Exception as e:
            print(f"⚠️  Error loading Edge Impulse model: {e}")
            print("   Switching to fallback inference mode...")
            self._setup_fallback_mode()
    
    def _load_edge_impulse_model(self):
        """Load Edge Impulse model using edge-impulse-python-sdk"""
        try:
            import edge_impulse_linux
            print("✓ Edge Impulse SDK loaded successfully")
            self.model = edge_impulse_linux
            print("✓ Edge Impulse ECG model initialized for edge inference")
        except ImportError:
            raise ImportError("edge-impulse-sdk not installed")
    
    def _setup_fallback_mode(self):
        """Setup fallback inference without Edge Impulse SDK"""
        # Fallback using normalization and threshold-based detection
        print("✓ Fallback inference mode: Using statistical ECG analysis")
        self.use_model = "fallback"
    
    def preprocess_ecg_features(self, mean: float, std: float, 
                               min_val: float, max_val: float, 
                               median: float) -> np.ndarray:
        """
        Preprocess ECG features for model input
        Normalizes features to [-1, 1] range (typical for Edge Impulse models)
        
        Args:
            mean: ECG signal mean
            std: ECG signal standard deviation
            min_val: ECG signal minimum
            max_val: ECG signal maximum
            median: ECG signal median
            
        Returns:
            Normalized feature array
        """
        # Normalize features to [-1, 1] range
        features = np.array([mean, std, min_val, max_val, median], dtype=np.float32)
        
        # Min-max normalization to [-1, 1]
        feature_min = np.min(features) if np.min(features) != 0 else -1
        feature_max = np.max(features) if np.max(features) != 0 else 1
        
        if feature_max != feature_min:
            normalized = 2 * ((features - feature_min) / (feature_max - feature_min)) - 1
        else:
            normalized = features
        
        return normalized.reshape(1, -1)
    
    def predict(self, mean: float, std: float, min_val: float, 
                max_val: float, median: float) -> Tuple[str, float]:
        """
        Run inference on ECG features
        
        Args:
            mean: ECG signal mean
            std: ECG signal standard deviation
            min_val: ECG signal minimum
            max_val: ECG signal maximum
            median: ECG signal median
            
        Returns:
            Tuple of (prediction, confidence)
            prediction: "Normal" or "Abnormal"
            confidence: Confidence score (0.0-1.0)
        """
        try:
            # Preprocess
            features = self.preprocess_ecg_features(mean, std, min_val, max_val, median)
            
            if self.use_model == "edge" and self.model is not None:
                return self._edge_impulse_predict(features)
            else:
                return self._fallback_predict(mean, std, min_val, max_val, median)
                
        except Exception as e:
            print(f"⚠️  Prediction error: {e}, using fallback...")
            return self._fallback_predict(mean, std, min_val, max_val, median)
    
    def _edge_impulse_predict(self, features: np.ndarray) -> Tuple[str, float]:
        """
        Run inference using Edge Impulse SDK
        """
        try:
            # Edge Impulse model inference
            # This assumes the model is properly deployed in edge-impulse-sdk
            # Placeholder for actual Edge Impulse API call
            
            # Example inference call (adapt to your specific Edge Impulse SDK version)
            result = self.model.classify(features)
            
            if result.get("classification"):
                predictions = result["classification"]
                # Get class with highest confidence
                best_class = max(predictions, key=predictions.get)
                confidence = predictions[best_class]
                
                prediction = "Abnormal" if best_class == 1 or best_class == "Abnormal" else "Normal"
                return prediction, float(confidence)
            else:
                raise ValueError("No classification results from Edge Impulse")
                
        except Exception as e:
            print(f"⚠️  Edge Impulse inference failed: {e}")
            raise
    
    def _fallback_predict(self, mean: float, std: float, min_val: float,
                         max_val: float, median: float) -> Tuple[str, float]:
        """
        Fallback inference using statistical analysis
        Detects abnormal ECG patterns based on feature statistics
        """
        # Abnormality scoring based on ECG feature characteristics
        abnormality_score = 0.0
        
        # High std deviation (signal variability) indicates abnormality
        if std > 0.8:
            abnormality_score += 0.3
        
        # Large amplitude range indicates abnormality
        amplitude_range = max_val - min_val
        if amplitude_range > 2.0:
            abnormality_score += 0.3
        
        # ECG signal far from zero typically indicates abnormality
        if abs(mean) > 0.3:
            abnormality_score += 0.2
        
        # Check for signal symmetry (median close to mean)
        if abs(median - mean) > 0.2:
            abnormality_score += 0.2
        
        # Determine prediction
        threshold = 0.5
        if abnormality_score >= threshold:
            prediction = "Abnormal"
            confidence = min(abnormality_score, 1.0)
        else:
            prediction = "Normal"
            confidence = 1.0 - abnormality_score
        
        return prediction, confidence
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "model_type": "Edge Impulse ECG Detector",
            "inference_type": self.use_model,
            "output_classes": self.output_classes,
            "input_features": 5,  # mean, std, min, max, median
            "edge_optimized": True,
            "resource_efficient": True
        }


class EdgeComputingManager:
    """
    Manages edge computing aspects:
    - On-device preprocessing
    - Data compression
    - Local caching
    - Bandwidth optimization
    """
    
    def __init__(self):
        self.local_cache = []
        self.max_cache_size = 100
        self.predictions_cache = {}
    
    def preprocess_at_edge(self, ecg_signal: np.ndarray) -> Dict[str, float]:
        """
        Extract ECG features at edge device
        Reduces data transmission bandwidth
        """
        if ecg_signal is None or len(ecg_signal) == 0:
            return None
        
        return {
            "mean": float(np.mean(ecg_signal)),
            "std": float(np.std(ecg_signal)),
            "min": float(np.min(ecg_signal)),
            "max": float(np.max(ecg_signal)),
            "median": float(np.median(ecg_signal))
        }
    
    def cache_prediction(self, features_hash: str, prediction: Tuple[str, float]):
        """Cache prediction results locally"""
        self.predictions_cache[features_hash] = prediction
        
        if len(self.predictions_cache) > self.max_cache_size:
            # Remove oldest entry
            oldest_key = next(iter(self.predictions_cache))
            del self.predictions_cache[oldest_key]
    
    def get_cached_prediction(self, features_hash: str) -> Tuple[str, float]:
        """Retrieve cached prediction"""
        return self.predictions_cache.get(features_hash)
    
    def calculate_compression_ratio(self, original_size: int, compressed_size: int) -> float:
        """Calculate data compression ratio"""
        if original_size == 0:
            return 0.0
        return (1 - compressed_size / original_size) * 100
    
    def get_edge_statistics(self) -> Dict[str, Any]:
        """Get edge computing statistics"""
        return {
            "cached_predictions": len(self.predictions_cache),
            "cache_size": self.max_cache_size,
            "edge_optimization_active": True
        }


# Initialize global edge model instance
edge_model = None
edge_manager = None

def initialize_edge_model():
    """Initialize edge model and manager"""
    global edge_model, edge_manager
    
    edge_model = EdgeImpulseECGModel()
    edge_manager = EdgeComputingManager()
    
    print("✓ Edge computing infrastructure initialized")
    return edge_model, edge_manager


def predict_ecg_anomaly(mean: float, std: float, min_val: float,
                        max_val: float, median: float) -> Tuple[str, float]:
    """
    Convenient wrapper for ECG anomaly prediction
    
    Returns:
        Tuple of (prediction, confidence)
    """
    global edge_model
    
    if edge_model is None:
        initialize_edge_model()
    
    return edge_model.predict(mean, std, min_val, max_val, median)


if __name__ == "__main__":
    # Test the edge model
    print("\n" + "=" * 60)
    print("🚀 Edge Impulse ECG Model Test")
    print("=" * 60)
    
    # Initialize
    model, manager = initialize_edge_model()
    
    # Test with sample normal ECG
    print("\n[Test 1] Normal ECG Pattern:")
    pred, conf = model.predict(mean=-0.025, std=0.585, min_val=-0.988, max_val=1.219, median=-0.034)
    print(f"  Prediction: {pred} (Confidence: {conf:.2%})")
    
    # Test with sample abnormal ECG
    print("\n[Test 2] Abnormal ECG Pattern:")
    pred, conf = model.predict(mean=-0.214, std=1.025, min_val=-2.443, max_val=2.221, median=0.175)
    print(f"  Prediction: {pred} (Confidence: {conf:.2%})")
    
    # Show model info
    print("\n[Model Info]:")
    info = model.get_model_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # Show edge statistics
    print("\n[Edge Computing Statistics]:")
    stats = manager.get_edge_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
