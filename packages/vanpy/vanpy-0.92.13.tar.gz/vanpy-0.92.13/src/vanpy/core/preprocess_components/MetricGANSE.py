import os

import pandas as pd
from yaml import YAMLObject
from vanpy.core.ComponentPayload import ComponentPayload
from vanpy.core.preprocess_components.BaseSegmenterComponent import BaseSegmenterComponent
from vanpy.utils.utils import create_dirs_if_not_exist, cut_segment, get_audio_files_paths
import time
import torch


class MetricGANSE(BaseSegmenterComponent):
    """
    Speech enhancement component using MetricGAN model.

    Enhances audio quality by reducing noise and improving speech clarity using
    the MetricGAN+ model from SpeechBrain.

    :ivar model: Loaded MetricGAN enhancement model instance.
    """
    model = None

    def __init__(self, yaml_config: YAMLObject):
        super().__init__(component_type='preprocessing', component_name='metricgan_se',
                         yaml_config=yaml_config)

    def load_model(self):
        """
        Load the MetricGAN enhancement model.
        """
        from speechbrain.pretrained import SpectralMaskEnhancement
        if torch.cuda.is_available():
            self.model = SpectralMaskEnhancement.from_hparams(source="speechbrain/metricgan-plus-voicebank",
                                                          savedir="pretrained_models/metricgan-plus-voicebank",
                                                          run_opts={"device": "cuda"})
        else:
            self.model = SpectralMaskEnhancement.from_hparams(source="speechbrain/metricgan-plus-voicebank",
                                                              savedir="pretrained_models/metricgan-plus-voicebank",)
        self.logger.info(f'Loaded model to {"GPU" if torch.cuda.is_available() else "CPU"}')

    def process_item(self, f, processed_path, input_column, output_dir):
        """
        Process a single audio file for speech enhancement.

        :param f: Path to the audio file.
        :param processed_path: Column name for output file paths.
        :param input_column: Column name for input file paths.
        :param output_dir: Directory to save enhanced audio.
        :return: DataFrame containing enhanced audio information.
        """
        import torch
        import torchaudio

        output_file = f'{output_dir}/{f.split("/")[-1]}'
        t_start_segmentation = time.time()

        # Load and add fake batch dimension
        noisy = self.model.load_audio(f).unsqueeze(0)

        # Add relative length tensor
        enhanced = self.model.enhance_batch(noisy, lengths=torch.tensor([1.]))

        # Saving enhanced signal on disk
        torchaudio.save(output_file, enhanced.cpu(), self.config['sampling_rate'])
        t_end_segmentation = time.time()

        f_d = {processed_path: [output_file], input_column: [f]}
        self.add_performance_metadata(f_d, t_start_segmentation, t_end_segmentation)
        f_df = pd.DataFrame.from_dict(f_d)
        return f_df

    def process(self, input_payload: ComponentPayload) -> ComponentPayload: 
        """
        Process audio files for speech enhancement.

        :param input_payload: Input payload containing audio files and metadata.
        :return: Output payload containing enhanced audio information.
        """
        if not self.model:
            self.load_model()

        metadata, df = input_payload.unpack()
        input_column = metadata['paths_column']
        paths_list = df[input_column].dropna().tolist()
        output_dir = self.config['output_dir']
        create_dirs_if_not_exist(output_dir)

        processed_path = self.get_processed_path()
        np_df, paths_list = self.get_file_paths_and_processed_df_if_not_overwriting(paths_list, processed_path,
                                                                                   input_column, output_dir)
        metadata = self.add_processed_path_to_metadata(self.get_processed_path(), metadata)
        metadata = self.add_performance_column_to_metadata(metadata)

        if not paths_list:
            self.logger.warning('You\'ve supplied an empty list to process')
            df = pd.merge(left=df, right=p_df, how='left', on=input_column)
            return ComponentPayload(metadata=metadata, df=df)

        p_df = self.process_with_progress(paths_list, metadata, processed_path,
                                          input_column, output_dir)

        MetricGANSE.cleanup_softlinks()
        df = pd.merge(left=df, right=p_df, how='left', on=input_column)
        return ComponentPayload(metadata=metadata, df=df)

    @staticmethod
    def cleanup_softlinks():
        """
        Clean up temporary softlinks created during processing.
        """
        for link in os.listdir():
            if '.wav' in link and os.path.islink(link):
                os.unlink(link)
