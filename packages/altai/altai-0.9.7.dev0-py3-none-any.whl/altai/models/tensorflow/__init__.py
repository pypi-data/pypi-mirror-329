from altai.utils.missing_optional_dependency import import_optional

ADULTEncoder, ADULTDecoder, MNISTEncoder, MNISTDecoder, MNISTClassifier = import_optional(
    'altai.models.tensorflow.cfrl_models',
    names=['ADULTEncoder', 'ADULTDecoder', 'MNISTEncoder', 'MNISTDecoder', 'MNISTClassifier'])

HeAE, AE = import_optional('altai.models.tensorflow.autoencoder', names=['HeAE', 'AE'])
Actor, Critic = import_optional('altai.models.tensorflow.actor_critic', names=['Actor', 'Critic'])
