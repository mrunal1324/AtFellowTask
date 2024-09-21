import React from 'react';
import {
  FacebookShareButton,
  FacebookIcon,
  TwitterShareButton,
  TwitterIcon,
  WhatsappShareButton,
  WhatsappIcon,
} from 'react-share';

function SocialShare({ itineraryUrl }) {
  return (
    <div>
      <FacebookShareButton url={itineraryUrl}>
        <FacebookIcon size={32} round />
      </FacebookShareButton>
      <TwitterShareButton url={itineraryUrl}>
        <TwitterIcon size={32} round />
      </TwitterShareButton>
      <WhatsappShareButton url={itineraryUrl}>
        <WhatsappIcon size={32} round />
      </WhatsappShareButton>
    </div>
  );
}

export default SocialShare;
