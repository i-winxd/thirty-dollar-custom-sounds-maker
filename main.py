import mimetypes
import os
from dataclasses import dataclass
from typing import Optional

import constants
import base64
import json


# interface ExportCustomSound {
#     soundName: string;
#     imgBits: string;
#     soundBits: string;
# }

# IMAGE_FORMATS, AUDIO_FORMATS
def contains_special_characters(input_string: str) -> bool:
    special_characters = "\'\"!@#$%^&*()\n "

    for char in input_string:
        if char in special_characters:
            return True

    return False


@dataclass
class ExportCustomSound:
    sound_name: str
    img_bits: str
    sound_bits: str

    def export_dict(self) -> dict[str, str]:
        return {"soundName": self.sound_name, "imgBits": self.img_bits,
                "soundBits": self.sound_bits}


@dataclass
class ImageAudioPair:
    path_to_img: str  # path_to
    path_to_audio: str  # path_to

    def export_items(self) -> Optional[ExportCustomSound]:
        name = os.path.splitext(os.path.basename(self.path_to_img))[0]
        image_data_url = file_to_data_url(self.path_to_img)
        if image_data_url is None:
            print(f"Unable to convert {self.path_to_img}")
            return None
        audio_data_url = file_to_data_url(self.path_to_audio)
        if audio_data_url is None:
            print(f"Unable to convert {self.path_to_img}")
            return None
        return ExportCustomSound(name, image_data_url, audio_data_url)


def file_to_data_url(file_path: str) -> Optional[str]:
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type:
        with open(file_path, 'rb') as file:
            file_contents = file.read()
            base64_encoded = base64.b64encode(file_contents).decode('utf-8')
            data_url = f'data:{mime_type};base64,{base64_encoded}'
            return data_url
    else:
        print("Unable to determine MIME type.")


class CandidateFile:
    path: str  # ANY path
    name: str  # basename, no extension. e.g. path/to/file.mp3 -> file
    extension: str  # extension only. e.g. path/to/file.mp3 -> .mp3 include the dot

    def __init__(self, path) -> None:
        self.path = path
        self.name = os.path.splitext(os.path.basename(path))[0]
        self.extension = os.path.splitext(path)[1]


def get_all_files_recursive(directory: str) -> list[str]:
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


def create_image_audio_pairs(audio_candidates: list[CandidateFile], image_candidates: list[CandidateFile]) -> list[
    ImageAudioPair]:
    image_audio_pairs = []
    paired_names = set()

    for audio_candidate in audio_candidates:
        if audio_candidate.name in paired_names:
            continue  # Skip if the name is already paired

        for image_candidate in image_candidates:
            if (
                    audio_candidate.name == image_candidate.name
            ):
                pair = ImageAudioPair(image_candidate.path, audio_candidate.path)
                image_audio_pairs.append(pair)
                paired_names.add(audio_candidate.name)

    return image_audio_pairs


def create_image_audio_pairs_eff(audio_candidates: list[CandidateFile], image_candidates: list[CandidateFile]) -> list[
    ImageAudioPair]:
    audio_candidates.sort(key=lambda x: x.name)
    image_candidates.sort(key=lambda x: x.name)
    audio_index = 0
    image_index = 0
    image_audio_pairs = []

    while audio_index < len(audio_candidates) and image_index < len(image_candidates):
        audio_candidate = audio_candidates[audio_index]
        image_candidate = image_candidates[image_index]

        if audio_candidate.name == image_candidate.name:
            pair = ImageAudioPair(image_candidate.path, audio_candidate.path)
            image_audio_pairs.append(pair)

            paired_name = audio_candidate.name

            # Move to the next candidates with the same name
            while audio_index < len(audio_candidates) and audio_candidates[audio_index].name == paired_name:
                audio_index += 1

            while image_index < len(image_candidates) and image_candidates[image_index].name == paired_name:
                image_index += 1
        elif audio_candidate.name < image_candidate.name:
            audio_index += 1
        else:
            image_index += 1

    return image_audio_pairs


def main() -> None:
    all_files = get_all_files_recursive('.')
    candidates_0 = [CandidateFile(x) for x in all_files]
    candidates_01 = [x for x in candidates_0 if not contains_special_characters(x.name)]
    candidates_image = [x for x in candidates_01 if x.extension in constants.IMAGE_FORMATS]
    candidates_audio = [x for x in candidates_01 if x.extension in constants.AUDIO_FORMATS]
    image_audio_pairs = create_image_audio_pairs_eff(candidates_audio, candidates_image)
    export_candidates_0 = [x.export_items() for x in image_audio_pairs]
    export_candidates_1 = [x for x in export_candidates_0 if x is not None]
    export_candidates_2 = [x.export_dict() for x in export_candidates_1]
    export_candidate_wrapped = {"exports": export_candidates_2}
    with open("EXPORTED_THIRTYDOLLAR.json", "w", encoding="UTF-8") as f:
        json.dump(export_candidate_wrapped, f, indent=4)
    print(f"Exported a total of {len(export_candidates_2)} custom sounds.")


if __name__ == '__main__':
    main()
