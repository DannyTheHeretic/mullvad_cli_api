

from dataclasses import dataclass


@dataclass
class DNS:
    """DNS Settings."""

    block_ads:bool = False
    block_trackers:bool = False
    block_malware:bool = False
    block_adult_content:bool = False
    block_gambling:bool = False
    block_social_media:bool = False

    def __dict__(self) -> dict:
        return {
            "--block-ads":self.block_ads,
            "--block-trackers":self.block_trackers,
            "--block-malware":self.block_malware,
            "--block-adult-content":self.block_adult_content,
            "--block-gambling":self.block_gambling, 
            "--block-social-media":self.block_social_media,
        }

    def __str__(self) -> str:
        t = self.__dict__()
        for i in t:
            print(i)
        return ""
