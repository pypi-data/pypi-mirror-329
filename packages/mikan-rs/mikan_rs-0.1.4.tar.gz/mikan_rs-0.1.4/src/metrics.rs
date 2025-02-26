use nii::Nifti1Image;
use std::collections::BTreeMap;

use crate::utils::{argwhere, get_binary_edge, get_percentile, mean};
use kdtree::distance::squared_euclidean;
use kdtree::KdTree;
use log::warn;
use ndarray::prelude::*;
use ndarray_stats::QuantileExt;
use rayon::prelude::*;

/// A structure to calculate various metrics based on confusion matrix for binary classification or segmentation tasks.
#[derive(Debug, Clone)]
pub struct ConfusionMatrix {
    tp_count: f64,
    tn_count: f64,
    fp_count: f64,
    fn_count: f64,
    label: u8,
}

impl ConfusionMatrix {
    /// init ConfusionMatrix using two segmentation mask, can be used for segmentation task
    pub fn new(gt: &Nifti1Image<u8>, pred: &Nifti1Image<u8>, label: u8) -> Self {
        let gt_arr = gt.ndarray();
        let pred_arr = pred.ndarray();
        ConfusionMatrix::new_from_ndarray(gt_arr.view(), pred_arr.view(), label)
    }

    pub fn new_from_ndarray(gt: ArrayView3<u8>, pred: ArrayView3<u8>, label: u8) -> Self {
        let gt_slice = gt.as_slice().unwrap();
        let pred_slice = pred.as_slice().unwrap();

        let (tp, fp, fn_, tn) = gt_slice
            .par_iter()
            .zip(pred_slice.par_iter())
            .fold(
                || (0u64, 0u64, 0u64, 0u64),
                |(mut tp, mut fp, mut fn_, mut tn), (&a, &b)| {
                    match (a == label, b == label) {
                        (true, true) => tp += 1,
                        (false, true) => fp += 1,
                        (true, false) => fn_ += 1,
                        (false, false) => tn += 1,
                    }
                    (tp, fp, fn_, tn)
                },
            )
            .reduce(
                || (0, 0, 0, 0),
                |(a1, b1, c1, d1), (a2, b2, c2, d2)| (a1 + a2, b1 + b2, c1 + c2, d1 + d2),
            );

        ConfusionMatrix {
            tp_count: tp as f64,
            fp_count: fp as f64,
            fn_count: fn_ as f64,
            tn_count: tn as f64,
            label,
        }
    }

    /// Recall/Sensitivity/Hit rate/True positive rate (TPR)
    pub fn get_senstivity(&self) -> f64 {
        if (self.tp_count + self.fn_count) == 0.0 {
            return 0.;
        }
        self.tp_count / (self.tp_count + self.fn_count)
    }

    /// Selectivity/Specificity/True negative rate (TNR)
    pub fn get_specificity(&self) -> f64 {
        if (self.tn_count + self.fp_count) == 0.0 {
            return 0.0;
        }
        self.tn_count / (self.tn_count + self.fp_count)
    }

    /// Precision/Positive predictive value (PPV)
    pub fn get_precision(&self) -> f64 {
        if (self.tp_count + self.fp_count) == 0.0 {
            return 0.0;
        }
        self.tp_count / (self.tp_count + self.fp_count)
    }
    /// accuracy/acc/Rand Index/RI/准确性
    pub fn get_accuracy(&self) -> f64 {
        if (self.tp_count + self.tn_count + self.fp_count + self.fn_count) == 0.0 {
            return 0.0;
        }
        (self.tp_count + self.tn_count)
            / (self.tp_count + self.tn_count + self.fp_count + self.fn_count)
    }

    /// balanced accuracy / BACC
    pub fn get_balanced_accuracy(&self) -> f64 {
        (self.get_senstivity() + self.get_specificity()) / 2.0
    }

    /// Dice/DSC
    pub fn get_dice(&self) -> f64 {
        if (2.0 * self.tp_count + self.fp_count + self.fn_count) == 0.0 {
            warn!(
                "label={}, Dice=0 due to TP: {}, FP: {}, FN: {}",
                self.label, self.tp_count, self.fp_count, self.fn_count
            );
            return 0.0;
        }
        (2.0 * self.tp_count) / (2.0 * self.tp_count + self.fp_count + self.fn_count)
    }

    /// f-score
    pub fn get_f_score(&self) -> f64 {
        if (2.0 * self.tp_count + self.fp_count + self.fn_count) == 0.0 {
            warn!(
                "label={}, f-score=0 due to TP: {}, FP: {}, FN: {}",
                self.label, self.tp_count, self.fp_count, self.fn_count
            );
            return 0.0;
        }
        (2.0 * self.tp_count) / (2.0 * self.tp_count + self.fp_count + self.fn_count)
    }

    /// f-beta score
    pub fn get_f_beta_score(&self, beta: u8) -> f64 {
        if ((1 + beta.pow(2)) as f64 * self.tp_count
            + beta.pow(2) as f64 * self.fn_count * self.fp_count)
            == 0.0
        {
            warn!(
                "label={}, f-beta-score=0 due to TP: {}, FP: {}, FN: {}",
                self.label, self.tp_count, self.fp_count, self.fn_count
            );
            return 0.0;
        }
        ((1 + beta.pow(2)) as f64 * self.tp_count)
            / ((1 + beta.pow(2)) as f64 * self.tp_count
                + beta.pow(2) as f64 * self.fn_count * self.fp_count)
    }

    /// jaccard score/IoU
    pub fn get_jaccard_score(&self) -> f64 {
        if (self.tp_count + self.fp_count + self.fn_count) == 0.0 {
            warn!(
                "label={}, jaccard=0 due to TP: {}, FP: {}, FN: {}",
                self.label, self.tp_count, self.fp_count, self.fn_count
            );
            return 0.0;
        }
        self.tp_count / (self.tp_count + self.fp_count + self.fn_count)
    }

    /// fnr
    pub fn get_fnr(&self) -> f64 {
        if (self.fn_count + self.tp_count) == 0.0 {
            warn!(
                "label={}, fnr=0 due to FP: {}, FN: {}",
                self.label, self.tp_count, self.fn_count
            );
            return 0.0;
        }
        self.fn_count / (self.fn_count + self.tp_count)
    }

    /// fpr
    pub fn get_fpr(&self) -> f64 {
        if (self.fp_count + self.tn_count) == 0.0 {
            warn!(
                "fpr=0 due to TP: {}, FP: {}, FN: {}",
                self.tp_count, self.fp_count, self.fn_count
            );
            return 0.0;
        }
        self.fp_count / (self.fp_count + self.tn_count)
    }

    /// volume similarity/VS/体积相似性
    pub fn get_volume_similarity(&self) -> f64 {
        if (2.0 * self.tp_count + self.fp_count + self.fn_count) == 0.0 {
            warn!(
                "label={}, vs=0 due to TP: {}, FP: {}, FN: {}",
                self.label, self.tp_count, self.fp_count, self.fn_count
            );
            return 0.0;
        }
        1.0 - (self.fn_count - self.fp_count).abs()
            / (2.0 * self.tp_count + self.fp_count + self.fn_count)
    }

    /// AUC/AUC_trapezoid/binary label AUC
    pub fn get_auc(&self) -> f64 {
        1.0 - 0.5 * (self.get_fpr() + self.get_fnr())
    }

    /// KAP/Kappa/CohensKapp
    pub fn get_kappa(&self) -> f64 {
        let sum_ = self.tp_count + self.tn_count + self.fp_count + self.fn_count;
        let fa = self.tp_count + self.tn_count;
        let fc = ((self.tn_count + self.fn_count) * (self.tn_count + self.fp_count)
            + (self.fp_count + self.tp_count) * (self.fn_count + self.tp_count))
            / sum_;
        if (sum_ - fc) == 0.0 {
            warn!(
                "label={}, kappa=0 due to TP: {}, FP: {}, FN: {}",
                self.label, self.tp_count, self.fp_count, self.fn_count
            );
            return 0.0;
        }
        (fa - fc) / (sum_ - fc)
    }

    pub fn get_mcc(&self) -> f64 {
        let top = self.tp_count * self.tn_count - self.fp_count * self.fn_count;

        // very huge
        let bot_raw = (self.tp_count + self.fp_count)
            * (self.tp_count + self.fn_count)
            * (self.tn_count + self.fp_count)
            * (self.tn_count + self.fn_count);
        if bot_raw == 0.0 {
            warn!(
                "label={}, mcc=0 due to TP: {}, FP: {}, FN: {}",
                self.label, self.tp_count, self.fp_count, self.fn_count
            );
        }
        let bot = bot_raw.sqrt();
        top / bot
    }

    pub fn get_nmcc(&self) -> f64 {
        let mcc = self.get_mcc();
        (mcc + 1.0) / 2.0
    }

    pub fn get_amcc(&self) -> f64 {
        self.get_mcc().abs()
    }

    /// adjust rand score/adjust rand index/ARI
    pub fn get_adjust_rand_score(&self) -> f64 {
        let top = self.tp_count * self.tn_count - self.fp_count * self.fn_count;
        let bot = (self.tp_count + self.fn_count) * (self.fn_count + self.tn_count)
            + (self.tp_count + self.fp_count) * (self.fp_count + self.tn_count);
        if bot == 0.0 {
            warn!(
                "label={}, ARI=0 due to TP: {}, FP: {}, FN: {}",
                self.label, self.tp_count, self.fp_count, self.fn_count
            );
            return 0.0;
        }
        2.0 * top / bot
    }

    pub fn get_all(&self) -> BTreeMap<String, f64> {
        let mut map = BTreeMap::new();
        map.insert("tp".to_string(), self.tp_count);
        map.insert("tn".to_string(), self.tn_count);
        map.insert("fp".to_string(), self.fp_count);
        map.insert("fn".to_string(), self.fn_count);
        map.insert("senstivity".to_string(), self.get_senstivity());
        map.insert("specificity".to_string(), self.get_specificity());
        map.insert("precision".to_string(), self.get_precision());
        map.insert("accuracy".to_string(), self.get_accuracy());
        map.insert(
            "balanced_accuracy".to_string(),
            self.get_balanced_accuracy(),
        );
        map.insert("dice".to_string(), self.get_dice());
        map.insert("f_score".to_string(), self.get_f_score());
        map.insert("jaccard_score".to_string(), self.get_jaccard_score());
        map.insert("fnr".to_string(), self.get_fnr());
        map.insert("fpr".to_string(), self.get_fpr());
        map.insert(
            "volume_similarity".to_string(),
            self.get_volume_similarity(),
        );
        map.insert("auc".to_string(), self.get_auc());
        map.insert("kappa".to_string(), self.get_kappa());
        map.insert("mcc".to_string(), self.get_mcc());
        map.insert("nmcc".to_string(), self.get_nmcc());
        map.insert("amcc".to_string(), self.get_amcc());
        map.insert(
            "adjust_rand_score".to_string(),
            self.get_adjust_rand_score(),
        );
        map
    }
}

struct KDTree {
    tree: KdTree<f64, usize, [f64; 3]>,
}

impl KDTree {
    fn new(points: &[(f64, f64, f64)]) -> Self {
        let mut kdtree = KdTree::new(3);
        for (idx, p) in points.iter().enumerate() {
            let point = [p.0 as f64, p.1 as f64, p.2 as f64];
            kdtree.add(point, idx).unwrap();
        }
        KDTree { tree: kdtree }
    }

    fn query(&self, points: &[(f64, f64, f64)]) -> Vec<f64> {
        points
            .par_iter()
            .map(|p| {
                let point = [p.0, p.1, p.2];
                let a = self.tree.nearest(&point, 1, &squared_euclidean).unwrap()[0];
                a.0 as f64
            })
            .collect()
    }
}

/// A structure to calculate various metrics based on distance for binary classification or segmentation tasks.
pub struct Distance {
    dist_pred_to_gt: Vec<f64>,
    dist_gt_to_pred: Vec<f64>,
}

impl Distance {
    pub fn new(gt: &Nifti1Image<u8>, pred: &Nifti1Image<u8>, label: u8) -> Self {
        // TODO: support different size, spacing, direction in the future, now we assume they are the same
        // Actually, having gt and pred in the same world space is enough
        assert_eq!(gt.get_size(), pred.get_size(), "Size mismatch");
        assert_eq!(gt.get_spacing(), pred.get_spacing(), "Spacing mismatch");
        assert_eq!(
            gt.get_direction(),
            pred.get_direction(),
            "Direction mismatch"
        );

        let spacing = gt.get_spacing().map(|x| x as f64);

        let gt_arr = gt.ndarray();
        let pred_arr = pred.ndarray();

        Distance::new_from_ndarray(gt_arr.view(), pred_arr.view(), spacing, label)
    }

    pub fn new_from_ndarray(
        gt_arr: ArrayView3<u8>,
        pred_arr: ArrayView3<u8>,
        spacing: [f64; 3],
        label: u8,
    ) -> Self {
        // Binarize
        let gt_arr = gt_arr.mapv(|x| if x == label { 1 } else { 0 });
        let pred_arr = pred_arr.mapv(|x| if x == label { 1 } else { 0 });

        // Get edge
        let gt_edge = get_binary_edge(&gt_arr);
        let pred_edge = get_binary_edge(&pred_arr);

        // Get edge argwhere
        let gt_argw: Vec<(usize, usize, usize)> = argwhere(&gt_edge, 1); // (z,y,x)
        let pred_argw: Vec<(usize, usize, usize)> = argwhere(&pred_edge, 1);

        // Convert to physical coordinates
        let gt_argw: Vec<(f64, f64, f64)> = gt_argw
            .par_iter()
            .map(|x| {
                let z = x.0 as f64 * spacing[2];
                let y = x.1 as f64 * spacing[1];
                let x = x.2 as f64 * spacing[0];
                (z, y, x)
            })
            .collect();

        let pred_argw: Vec<(f64, f64, f64)> = pred_argw
            .par_iter()
            .map(|x| {
                let z = x.0 as f64 * spacing[2];
                let y = x.1 as f64 * spacing[1];
                let x = x.2 as f64 * spacing[0];
                (z, y, x)
            })
            .collect();

        let dist_pred_to_gt = KDTree::new(&gt_argw).query(&pred_argw);
        let dist_gt_to_pred = KDTree::new(&pred_argw).query(&gt_argw);

        let dist_pred_to_gt = dist_pred_to_gt.par_iter().map(|x| x.sqrt()).collect(); // square
        let dist_gt_to_pred = dist_gt_to_pred.par_iter().map(|x| x.sqrt()).collect(); // square

        Distance {
            dist_pred_to_gt,
            dist_gt_to_pred,
        }
    }

    pub fn get_hausdorff_distance(&self) -> f64 {
        if self.dist_gt_to_pred.len() == 0 || self.dist_pred_to_gt.len() == 0 {
            warn!("hd=0 due to no voxels");
            return 0.0;
        }
        f64::max(
            Array::from(self.dist_pred_to_gt.clone())
                .max()
                .unwrap()
                .clone(),
            Array::from(self.dist_gt_to_pred.clone())
                .max()
                .unwrap()
                .clone(),
        )
    }

    pub fn get_hausdorff_distance_95(&self) -> f64 {
        if self.dist_gt_to_pred.len() == 0 || self.dist_pred_to_gt.len() == 0 {
            warn!("hd95=0 due to no voxels");
            return 0.0;
        }
        let mut dist_pred_to_gt = self.dist_pred_to_gt.clone();
        let mut dist_gt_to_pred = self.dist_gt_to_pred.clone();
        f64::max(
            get_percentile(&mut dist_pred_to_gt, 0.95),
            get_percentile(&mut dist_gt_to_pred, 0.95),
        )
    }

    pub fn get_assd(&self) -> f64 {
        if self.dist_gt_to_pred.len() == 0 || self.dist_pred_to_gt.len() == 0 {
            warn!("assd=0 due to no voxels");
            return 0.0;
        }
        let merged = self
            .dist_pred_to_gt
            .iter()
            .chain(self.dist_gt_to_pred.iter())
            .cloned()
            .collect();
        mean(&merged) as f64
    }

    pub fn get_masd(&self) -> f64 {
        if self.dist_gt_to_pred.len() == 0 || self.dist_pred_to_gt.len() == 0 {
            warn!("masd=0 due to no voxels");
            return 0.0;
        }
        ((mean(&self.dist_pred_to_gt) + mean(&self.dist_gt_to_pred)) / 2.0) as f64
    }

    pub fn get_all(&self) -> BTreeMap<String, f64> {
        let mut results = BTreeMap::new();
        results.insert(
            "hausdorff_distance".to_string(),
            self.get_hausdorff_distance(),
        );
        results.insert(
            "hausdorff_distance_95".to_string(),
            self.get_hausdorff_distance_95(),
        );
        results.insert("assd".to_string(), self.get_assd());
        results.insert("masd".to_string(), self.get_masd());
        results
    }
}

/// A ndarray api for python to calculate lots of metrics for given labels.
pub fn calc_metrics_use_ndarray(
    gt_arr: ArrayView3<u8>,
    pred_arr: ArrayView3<u8>,
    labels: &[u8],
    spacing: [f64; 3],
    with_distance: bool,
) -> Vec<BTreeMap<String, f64>> {
    let mut mat_results: Vec<BTreeMap<String, f64>> = labels
        .par_iter()
        .map(|&label| {
            let cm = ConfusionMatrix::new_from_ndarray(gt_arr, pred_arr, label);
            let mut all_results = cm.get_all();
            all_results.insert("label".to_string(), label as f64);
            all_results
        })
        .collect();

    if with_distance {
        let dist_results: Vec<BTreeMap<String, f64>> = labels
            .par_iter()
            .map(|&label| {
                let dst = Distance::new_from_ndarray(gt_arr, pred_arr, spacing, label);
                let mut all_results = dst.get_all();
                all_results.insert("label".to_string(), label as f64);
                all_results
            })
            .collect();
        for (map1, map2) in mat_results.iter_mut().zip(dist_results.iter()) {
            map1.extend(map2.iter().map(|(k, v)| (k.clone(), *v)));
        }
    }
    mat_results
}

#[cfg(test)]
mod test {

    use super::*;
    use std::error::Error;
    use std::path::Path;
    use std::time::Instant;

    #[test]
    fn test_matrix_from_image() -> Result<(), Box<dyn Error>> {
        let gt = Path::new(r"data\patients_26_ground_truth.nii.gz");
        let pred = Path::new(r"data\patients_26_segmentation.nii.gz");

        let gt = nii::read_image::<u8>(gt);
        let pred = nii::read_image::<u8>(pred);

        let t = Instant::now();

        // let unique_labels = merge_vector(unique(&gt_arr), unique(&pred_arr), true);
        let unique_labels = [1, 2, 3, 4, 5];

        let results: Vec<BTreeMap<String, f64>> = unique_labels
            .par_iter()
            .map(|&label| {
                let cm = ConfusionMatrix::new(&gt, &pred, label);
                let mut all_results = cm.get_all();
                all_results.insert("label".to_string(), label as f64);
                all_results
            })
            .collect();
        println!("{:?}", results);
        println!("Cost {:?} ms", t.elapsed().as_millis());

        Ok(())
    }

    #[test]
    fn test_distances() -> Result<(), Box<dyn Error>> {
        let gt = Path::new(r"data\patients_26_ground_truth.nii.gz");
        let pred = Path::new(r"data\patients_26_segmentation.nii.gz");

        let gt = nii::read_image::<u8>(gt);
        let pred = nii::read_image::<u8>(pred);

        let t = Instant::now();

        let label = 1;
        let dist = Distance::new(&gt, &pred, label);

        let hd = dist.get_hausdorff_distance();
        let hd95 = dist.get_hausdorff_distance_95();
        let assd = dist.get_assd();
        let masd = dist.get_masd();

        println!("Hausdorff distance: {} mm", hd);
        println!("Hausdorff distance 95%: {} mm", hd95);
        println!("Average Symmetric Surface Distance: {} mm", assd);
        println!("Mean Average Surface Distance: {} mm", masd);
        println!("Cost {:?} ms", t.elapsed().as_millis());

        Ok(())
    }

    #[test]
    fn test_mp_distances() -> Result<(), Box<dyn Error>> {
        let gt = Path::new(r"data\patients_26_ground_truth.nii.gz");
        let pred = Path::new(r"data\patients_26_segmentation.nii.gz");

        let gt = nii::read_image::<u8>(gt);
        let pred = nii::read_image::<u8>(pred);

        let t = Instant::now();

        let label: Vec<u8> = vec![1, 2, 3, 4, 5];

        let results: Vec<f64> = label
            .par_iter()
            .map(|label| {
                let dist = Distance::new(&gt, &pred, *label);
                dist.get_hausdorff_distance_95()
            })
            .collect();

        println!("Hausdorff distance 95: {:?} mm", results);
        println!("Cost {:?} ms", t.elapsed().as_millis());

        Ok(())
    }
}
