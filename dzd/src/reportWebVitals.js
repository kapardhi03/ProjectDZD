import { loadModel } from './modelLoader';

export async function detectZeroDayAttack(file) {
  const model1 = await loadModel('./Models/RandomForestmodel');
  const model2 = await loadModel('./Models/bot_model.pkl');
  const model3 = await loadModel('./Models/ddoshulk_model.pkl');
  const model4 = await loadModel('./Models/dos_goldeneye_model.pkl');
  const model5 = await loadModel('./Models/dos_slowhttptest_model.pkl');
  const model6 = await loadModel('./Models/dos_slowloris_model.pkl');
  const model7 = await loadModel('./Models/FTP-PATATOR_model.pkl');
  const model8 = await loadModel('./Models/infiltration_model.pkl');
  const model9 = await loadModel('./Models/ssh_patator_model.pkl');
  const model10 = await loadModel('./Models/webattack_bruteforce_model.pkl');
  const model11 = await loadModel('./Models/webattack_sqlinjection_model.pkl');
  const model12 = await loadModel('./Models/ddos_model.pkl');

  for (const modelPath of isolationForestModelPaths) {
    const isolationForestModel = await tf.loadLayersModel(modelPath);
    isolationForestModels.push(isolationForestModel);
  }

  // Apply the LSTM model on the input file
  const lstmPredictions = RandomForestmodel.predict(file);

  // Determine if the input file is malicious or benign
  const isMalicious = lstmPredictions > 0.5;

  if (isMalicious) {
    let attackType = 'Unknown';

    // Apply the Isolation Forest models to detect the type of attack
    for (let i = 0; i < isolationForestModels.length; i++) {
      const isolationForestModel = isolationForestModels[i];
      const isolationForestPrediction = isolationForestModel.predict(file);

      if (isolationForestPrediction > 0.5) {
        // Set the detected attack type based on the model index
        attackType = getAttackType(i);
        break;
      }
    }

    // Return the detected attack type
    return attackType;
  }

  // If the file is benign, return null
  return null;
};
