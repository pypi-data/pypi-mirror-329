import requests
from bs4 import BeautifulSoup
import json
import re
from typing import Dict, List, Optional, Tuple

class MediumProfileError(Exception):
    """Custom exception for Medium profile related errors"""
    pass

class MediumArticleFinder:
    """Finds and lists Medium articles without fetching their content"""

    def __init__(self):
        """Initialize with a requests session for connection reuse"""
        self.__session = requests.Session()
    
    def __make_http_request(self, url: str, method: str = 'GET', data: Optional[Dict] = None) -> Optional[requests.Response]:
        """Internal method: Make HTTP request using session"""
        try:
            if method.upper() == 'GET':
                response = self.__session.get(url, timeout=30)
            elif method.upper() == 'POST':
                if not data:
                    raise MediumProfileError("Data is required for POST request")
                response = self.__session.post(url, json=data, timeout=30)
            else:
                raise MediumProfileError(f"Unsupported HTTP method: {method}")
                
            response.raise_for_status()
            return response
            
        except requests.RequestException as e:
            print(f"HTTP request failed: {e}")
            return None
    
    @staticmethod
    def __extract_apollo_state(script_tag: str) -> Optional[str]:
        """Internal method: Extract Apollo state JSON string from script tag"""
        try:
            if "window.__APOLLO_STATE__ =" in script_tag:
                return script_tag.split("= ", 1)[1]
        except Exception:
            return None
        return None
    
    def __extract_next_page_token(self, script_tags: List[BeautifulSoup]) -> Optional[Dict]:
        """Internal method: Extract next page token from script tags"""
        try:
            for script in script_tags:
                if not script.string:
                    continue
                    
                json_str = self.__extract_apollo_state(script.string)
                if not json_str:
                    continue

                pattern = r'"pagingInfo":\s*{\s*"__typename":\s*"Paging",\s*"next":\s*({.*?})\s*}'
                match = re.search(pattern, json_str)
                
                if match:
                    return json.loads(match.group(1))['from']
                    
        except Exception as e:
            print(f"Error extracting next page token: {e}")
        return None
    
    @staticmethod
    def __parse_article_data(article_json: Dict, isHomePage: bool = True) -> Dict:
        """Internal method: Parse raw article JSON into structured format"""
        try:
            return {
                'id': article_json['id'],
                'title': article_json['title'],
                'description': article_json['extendedPreviewContent']['subtitle'],
                'thumbnail': {
                    'image_url': article_json['previewImage']['__ref'] if isHomePage else article_json['previewImage']['id'],
                    'alt_text': None
                },
                'url': article_json['mediumUrl'],
                'first_published_at': article_json['firstPublishedAt'],
                'latest_published_at': article_json['latestPublishedAt'],
                'read_time': article_json['readingTime'],
                'clap_count': article_json['clapCount'],
                'post_responses': article_json['postResponses']['count']
            }
        except KeyError as e:
            print(f"Error parsing article data: Missing key {e}")
            return {}
        
    def __fetch_initial_articles(self, username: str) -> Tuple[List[Dict], Optional[Dict]]:
        """Internal method: Fetch first page of articles"""
        try:
            url = f"https://medium.com/@{username}"
            response = self.__make_http_request(url)
            if not response:
                return [], None

            if "PAGE NOT FOUND" in response.text:
                print("Page not found")
                raise MediumProfileError(f"Profile not found for username: @{username}")

            soup = BeautifulSoup(response.text, "html.parser")
            script_tags = soup.find_all("script")
            
            apollo_state_data = None
            for script in script_tags:
                if not script.string:
                    continue
                    
                apollo_state_data = self.__extract_apollo_state(script.string)
                if apollo_state_data is not None:
                    break

            post_pattern = r'"Post:[^:]+":{"__typename":"Post".*?"pinnedByCreatorAt":[^}]+}'
            post_matches = re.findall(post_pattern, apollo_state_data)

            if not post_matches:
                return [], None
            
            raw_article_data = []
            for raw_post in post_matches:
                raw_article_data.append(json.loads('{' + raw_post + '}'))

            articles = []
            for article_json in raw_article_data:
                for _, article_data in article_json.items():
                    article = self.__parse_article_data(article_data)
                    if article:
                        articles.append(article)
                        
            next_page_token = self.__extract_next_page_token(script_tags)
            return articles, next_page_token
        
        except MediumProfileError:
            raise
            
        except Exception as e:
            raise MediumProfileError(f"Error fetching initial articles: {e}")
    
    def __fetch_more_articles(self, username: str, page_token: str) -> Tuple[List[Dict], Optional[str]]:
        """Internal method: Fetch additional articles using pagination token"""
        try:
            url = "https://medium.com/_/graphql"
            payload = [{
                "operationName": "UserProfileQuery",
                "variables": {
                    "homepagePostsFrom": page_token,
                    "includeDistributedResponses": True,
                    "id": None,
                    "username": username,
                    "homepagePostsLimit": 10,
                },
                "query": "query UserProfileQuery($id: ID, $username: ID, $homepagePostsLimit: PaginationLimit, $homepagePostsFrom: String = null, $includeDistributedResponses: Boolean = true) {\n  userResult(id: $id, username: $username) {\n    __typename\n    ... on User {\n      id\n      name\n      viewerIsUser\n      viewerEdge {\n        id\n        isFollowing\n        __typename\n      }\n      homePostsPublished: homepagePostsConnection(paging: {limit: 1}) {\n        posts {\n          id\n          __typename\n        }\n        __typename\n      }\n      ...UserCanonicalizer_user\n      ...MastodonVerificationLink_user\n      ...UserProfileScreen_user\n      __typename\n    }\n  }\n}\n\nfragment UserCanonicalizer_user on User {\n  id\n  username\n  hasSubdomain\n  customDomainState {\n    live {\n      domain\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment MastodonVerificationLink_user on User {\n  id\n  linkedAccounts {\n    mastodon {\n      domain\n      username\n      __typename\n      id\n    }\n    __typename\n    id\n  }\n  __typename\n}\n\nfragment UserProfileScreen_user on User {\n  __typename\n  id\n  viewerIsUser\n  ...PublisherHeader_publisher\n  ...PublisherHomepagePosts_publisher\n  ...UserProfileMetadata_user\n  ...SuspendedBannerLoader_user\n  ...useAnalytics_user\n  ...useIsVerifiedBookAuthor_user\n  ...UserProfileBooks_user\n}\n\nfragment PublisherHeader_publisher on Publisher {\n  id\n  ...PublisherHeaderBackground_publisher\n  ...PublisherHeaderNameplate_publisher\n  ...PublisherHeaderActions_publisher\n  ...PublisherHeaderNav_publisher\n  ...PublisherHeaderMenu_publisher\n  __typename\n}\n\nfragment PublisherHeaderBackground_publisher on Publisher {\n  __typename\n  id\n  customStyleSheet {\n    ...PublisherHeaderBackground_customStyleSheet\n    __typename\n    id\n  }\n  ... on Collection {\n    colorPalette {\n      tintBackgroundSpectrum {\n        backgroundColor\n        __typename\n      }\n      __typename\n    }\n    isAuroraVisible\n    legacyHeaderBackgroundImage {\n      id\n      originalWidth\n      focusPercentX\n      focusPercentY\n      __typename\n    }\n    ...collectionTintBackgroundTheme_collection\n    __typename\n    id\n  }\n  ...publisherUrl_publisher\n}\n\nfragment PublisherHeaderBackground_customStyleSheet on CustomStyleSheet {\n  id\n  global {\n    colorPalette {\n      background {\n        rgb\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  header {\n    headerScale\n    backgroundImageDisplayMode\n    backgroundImageVerticalAlignment\n    backgroundColorDisplayMode\n    backgroundColor {\n      alpha\n      rgb\n      ...getHexFromColorValue_colorValue\n      ...getOpaqueHexFromColorValue_colorValue\n      __typename\n    }\n    secondaryBackgroundColor {\n      ...getHexFromColorValue_colorValue\n      __typename\n    }\n    postBackgroundColor {\n      ...getHexFromColorValue_colorValue\n      __typename\n    }\n    backgroundImage {\n      id\n      originalWidth\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment getHexFromColorValue_colorValue on ColorValue {\n  rgb\n  alpha\n  __typename\n}\n\nfragment getOpaqueHexFromColorValue_colorValue on ColorValue {\n  rgb\n  __typename\n}\n\nfragment collectionTintBackgroundTheme_collection on Collection {\n  colorPalette {\n    ...collectionTintBackgroundTheme_colorPalette\n    __typename\n  }\n  customStyleSheet {\n    id\n    ...collectionTintBackgroundTheme_customStyleSheet\n    __typename\n  }\n  __typename\n  id\n}\n\nfragment collectionTintBackgroundTheme_colorPalette on ColorPalette {\n  ...customTintBackgroundTheme_colorPalette\n  __typename\n}\n\nfragment customTintBackgroundTheme_colorPalette on ColorPalette {\n  tintBackgroundSpectrum {\n    ...ThemeUtil_colorSpectrum\n    __typename\n  }\n  __typename\n}\n\nfragment ThemeUtil_colorSpectrum on ColorSpectrum {\n  backgroundColor\n  ...ThemeUtilInterpolateHelpers_colorSpectrum\n  __typename\n}\n\nfragment ThemeUtilInterpolateHelpers_colorSpectrum on ColorSpectrum {\n  colorPoints {\n    ...ThemeUtil_colorPoint\n    __typename\n  }\n  __typename\n}\n\nfragment ThemeUtil_colorPoint on ColorPoint {\n  color\n  point\n  __typename\n}\n\nfragment collectionTintBackgroundTheme_customStyleSheet on CustomStyleSheet {\n  id\n  ...customTintBackgroundTheme_customStyleSheet\n  __typename\n}\n\nfragment customTintBackgroundTheme_customStyleSheet on CustomStyleSheet {\n  id\n  global {\n    colorPalette {\n      primary {\n        colorPalette {\n          ...customTintBackgroundTheme_colorPalette\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment publisherUrl_publisher on Publisher {\n  id\n  __typename\n  ... on Collection {\n    ...collectionUrl_collection\n    __typename\n    id\n  }\n  ... on User {\n    ...userUrl_user\n    __typename\n    id\n  }\n}\n\nfragment collectionUrl_collection on Collection {\n  id\n  domain\n  slug\n  __typename\n}\n\nfragment userUrl_user on User {\n  __typename\n  id\n  customDomainState {\n    live {\n      domain\n      __typename\n    }\n    __typename\n  }\n  hasSubdomain\n  username\n}\n\nfragment PublisherHeaderNameplate_publisher on Publisher {\n  ...PublisherAvatar_publisher\n  ...PublisherHeaderLogo_publisher\n  ...PublisherHeaderName_publisher\n  ...PublisherFollowersCount_publisher\n  ...useLogo_publisher\n  __typename\n}\n\nfragment PublisherAvatar_publisher on Publisher {\n  __typename\n  ... on Collection {\n    id\n    ...CollectionAvatar_collection\n    __typename\n  }\n  ... on User {\n    id\n    ...UserAvatar_user\n    __typename\n  }\n}\n\nfragment CollectionAvatar_collection on Collection {\n  name\n  avatar {\n    id\n    __typename\n  }\n  ...collectionUrl_collection\n  __typename\n  id\n}\n\nfragment UserAvatar_user on User {\n  __typename\n  id\n  imageId\n  membership {\n    tier\n    __typename\n    id\n  }\n  name\n  username\n  ...userUrl_user\n}\n\nfragment PublisherHeaderLogo_publisher on Publisher {\n  __typename\n  id\n  name\n  ... on Collection {\n    logo {\n      id\n      __typename\n    }\n    __typename\n    id\n  }\n}\n\nfragment PublisherHeaderName_publisher on Publisher {\n  __typename\n  id\n  customStyleSheet {\n    id\n    header {\n      appNameColor {\n        ...getHexFromColorValue_colorValue\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  name\n  ... on User {\n    ...useIsVerifiedBookAuthor_user\n    ...UserPronouns_user\n    __typename\n    id\n  }\n}\n\nfragment useIsVerifiedBookAuthor_user on User {\n  verifications {\n    isBookAuthor\n    __typename\n  }\n  __typename\n  id\n}\n\nfragment UserPronouns_user on User {\n  pronouns\n  __typename\n  id\n}\n\nfragment PublisherFollowersCount_publisher on Publisher {\n  id\n  __typename\n  id\n  ... on Collection {\n    slug\n    subscriberCount\n    ...collectionUrl_collection\n    __typename\n    id\n  }\n  ... on User {\n    socialStats {\n      followerCount\n      __typename\n    }\n    username\n    ...userUrl_user\n    __typename\n    id\n  }\n}\n\nfragment useLogo_publisher on Publisher {\n  __typename\n  id\n  customStyleSheet {\n    id\n    header {\n      logoImage {\n        ...useLogo_imageMetadata\n        __typename\n      }\n      appNameTreatment\n      __typename\n    }\n    __typename\n  }\n  name\n  ... on Collection {\n    isAuroraVisible\n    logo {\n      ...useLogo_imageMetadata\n      __typename\n      id\n    }\n    __typename\n    id\n  }\n}\n\nfragment useLogo_imageMetadata on ImageMetadata {\n  __typename\n  id\n  originalHeight\n  originalWidth\n}\n\nfragment PublisherHeaderActions_publisher on Publisher {\n  __typename\n  ...PublisherHeaderMenu_publisher\n  ... on Collection {\n    ...CollectionFollowButton_collection\n    __typename\n    id\n  }\n  ... on User {\n    ...FollowAndSubscribeButtons_user\n    __typename\n    id\n  }\n}\n\nfragment PublisherHeaderMenu_publisher on Publisher {\n  __typename\n  ...MetaHeaderPubMenu_publisher\n}\n\nfragment MetaHeaderPubMenu_publisher on Publisher {\n  __typename\n  ... on Collection {\n    ...MetaHeaderPubMenu_publisher_collection\n    __typename\n    id\n  }\n  ... on User {\n    ...MetaHeaderPubMenu_publisher_user\n    __typename\n    id\n  }\n}\n\nfragment MetaHeaderPubMenu_publisher_collection on Collection {\n  id\n  slug\n  name\n  domain\n  newsletterV3 {\n    slug\n    __typename\n    id\n  }\n  ...MutePopoverOptions_collection\n  __typename\n}\n\nfragment MutePopoverOptions_collection on Collection {\n  id\n  __typename\n}\n\nfragment MetaHeaderPubMenu_publisher_user on User {\n  id\n  username\n  ...MutePopoverOptions_creator\n  __typename\n}\n\nfragment MutePopoverOptions_creator on User {\n  id\n  __typename\n}\n\nfragment CollectionFollowButton_collection on Collection {\n  __typename\n  id\n  name\n  slug\n  ...collectionUrl_collection\n  ...SusiClickable_collection\n}\n\nfragment SusiClickable_collection on Collection {\n  ...SusiContainer_collection\n  __typename\n  id\n}\n\nfragment SusiContainer_collection on Collection {\n  name\n  ...SignInOptions_collection\n  ...SignUpOptions_collection\n  __typename\n  id\n}\n\nfragment SignInOptions_collection on Collection {\n  id\n  name\n  __typename\n}\n\nfragment SignUpOptions_collection on Collection {\n  id\n  name\n  __typename\n}\n\nfragment FollowAndSubscribeButtons_user on User {\n  ...UserFollowButton_user\n  ...UserSubscribeButton_user\n  __typename\n  id\n}\n\nfragment UserFollowButton_user on User {\n  ...UserFollowButtonSignedIn_user\n  ...UserFollowButtonSignedOut_user\n  __typename\n  id\n}\n\nfragment UserFollowButtonSignedIn_user on User {\n  id\n  name\n  __typename\n}\n\nfragment UserFollowButtonSignedOut_user on User {\n  id\n  ...SusiClickable_user\n  __typename\n}\n\nfragment SusiClickable_user on User {\n  ...SusiContainer_user\n  __typename\n  id\n}\n\nfragment SusiContainer_user on User {\n  ...SignInOptions_user\n  ...SignUpOptions_user\n  __typename\n  id\n}\n\nfragment SignInOptions_user on User {\n  id\n  name\n  __typename\n}\n\nfragment SignUpOptions_user on User {\n  id\n  name\n  __typename\n}\n\nfragment UserSubscribeButton_user on User {\n  id\n  isPartnerProgramEnrolled\n  name\n  viewerEdge {\n    id\n    isFollowing\n    isUser\n    __typename\n  }\n  viewerIsUser\n  newsletterV3 {\n    id\n    ...useNewsletterV3Subscription_newsletterV3\n    __typename\n  }\n  ...useNewsletterV3Subscription_user\n  ...MembershipUpsellModal_user\n  __typename\n}\n\nfragment useNewsletterV3Subscription_newsletterV3 on NewsletterV3 {\n  id\n  type\n  slug\n  name\n  collection {\n    slug\n    __typename\n    id\n  }\n  user {\n    id\n    name\n    username\n    newsletterV3 {\n      id\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment useNewsletterV3Subscription_user on User {\n  id\n  username\n  newsletterV3 {\n    ...useNewsletterV3Subscription_newsletterV3\n    __typename\n    id\n  }\n  __typename\n}\n\nfragment MembershipUpsellModal_user on User {\n  id\n  name\n  imageId\n  postSubscribeMembershipUpsellShownAt\n  newsletterV3 {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment PublisherHeaderNav_publisher on Publisher {\n  __typename\n  id\n  customStyleSheet {\n    navigation {\n      navItems {\n        name\n        ...PublisherHeaderNavLink_headerNavigationItem\n        __typename\n      }\n      __typename\n    }\n    __typename\n    id\n  }\n  ...PublisherHeaderNavLink_publisher\n  ... on Collection {\n    domain\n    isAuroraVisible\n    slug\n    navItems {\n      tagSlug\n      title\n      url\n      __typename\n    }\n    __typename\n    id\n  }\n  ... on User {\n    customDomainState {\n      live {\n        domain\n        __typename\n      }\n      __typename\n    }\n    hasSubdomain\n    username\n    homePostsPublished: homepagePostsConnection(paging: {limit: 1}) {\n      posts {\n        id\n        __typename\n      }\n      __typename\n    }\n    ...useIsVerifiedBookAuthor_user\n    __typename\n    id\n  }\n}\n\nfragment PublisherHeaderNavLink_headerNavigationItem on HeaderNavigationItem {\n  href\n  name\n  tags {\n    id\n    normalizedTagSlug\n    __typename\n  }\n  type\n  __typename\n}\n\nfragment PublisherHeaderNavLink_publisher on Publisher {\n  __typename\n  id\n  ... on Collection {\n    slug\n    __typename\n    id\n  }\n}\n\nfragment PublisherHomepagePosts_publisher on Publisher {\n  __typename\n  id\n  homepagePostsConnection(\n    paging: {limit: $homepagePostsLimit, from: $homepagePostsFrom}\n    includeDistributedResponses: $includeDistributedResponses\n  ) {\n    posts {\n      ...StreamPostPreview_post\n      pinnedByCreatorAt\n      pinnedAt\n      __typename\n    }\n    pagingInfo {\n      next {\n        from\n        limit\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  ...NewsletterV3Promo_publisher\n  ...PublisherHomepagePosts_user\n}\n\nfragment StreamPostPreview_post on Post {\n  id\n  ...StreamPostPreviewContent_post\n  ...PostPreviewContainer_post\n  __typename\n}\n\nfragment StreamPostPreviewContent_post on Post {\n  id\n  title\n  previewImage {\n    id\n    __typename\n  }\n  extendedPreviewContent {\n    subtitle\n    __typename\n  }\n  ...StreamPostPreviewImage_post\n  ...PostPreviewFooter_post\n  ...PostPreviewByLine_post\n  ...PostPreviewInformation_post\n  __typename\n}\n\nfragment StreamPostPreviewImage_post on Post {\n  title\n  previewImage {\n    ...StreamPostPreviewImage_imageMetadata\n    __typename\n    id\n  }\n  __typename\n  id\n}\n\nfragment StreamPostPreviewImage_imageMetadata on ImageMetadata {\n  id\n  focusPercentX\n  focusPercentY\n  alt\n  __typename\n}\n\nfragment PostPreviewFooter_post on Post {\n  ...PostPreviewFooterSocial_post\n  ...PostPreviewFooterMenu_post\n  ...PostPreviewFooterMeta_post\n  __typename\n  id\n}\n\nfragment PostPreviewFooterSocial_post on Post {\n  id\n  ...MultiVote_post\n  allowResponses\n  isPublished\n  isLimitedState\n  postResponses {\n    count\n    __typename\n  }\n  __typename\n}\n\nfragment MultiVote_post on Post {\n  id\n  creator {\n    id\n    ...SusiClickable_user\n    __typename\n  }\n  isPublished\n  ...SusiClickable_post\n  collection {\n    id\n    slug\n    __typename\n  }\n  isLimitedState\n  ...MultiVoteCount_post\n  __typename\n}\n\nfragment SusiClickable_post on Post {\n  id\n  mediumUrl\n  ...SusiContainer_post\n  __typename\n}\n\nfragment SusiContainer_post on Post {\n  id\n  __typename\n}\n\nfragment MultiVoteCount_post on Post {\n  id\n  __typename\n}\n\nfragment PostPreviewFooterMenu_post on Post {\n  id\n  ...BookmarkButton_post\n  ...OverflowMenuButton_post\n  __typename\n}\n\nfragment BookmarkButton_post on Post {\n  visibility\n  ...SusiClickable_post\n  ...AddToCatalogBookmarkButton_post\n  __typename\n  id\n}\n\nfragment AddToCatalogBookmarkButton_post on Post {\n  ...AddToCatalogBase_post\n  __typename\n  id\n}\n\nfragment AddToCatalogBase_post on Post {\n  id\n  isPublished\n  ...SusiClickable_post\n  __typename\n}\n\nfragment OverflowMenuButton_post on Post {\n  id\n  visibility\n  ...OverflowMenu_post\n  __typename\n}\n\nfragment OverflowMenu_post on Post {\n  id\n  creator {\n    id\n    __typename\n  }\n  collection {\n    id\n    __typename\n  }\n  ...OverflowMenuItemUndoClaps_post\n  ...AddToCatalogBase_post\n  ...ExplicitSignalMenuOptions_post\n  __typename\n}\n\nfragment OverflowMenuItemUndoClaps_post on Post {\n  id\n  clapCount\n  ...ClapMutation_post\n  __typename\n}\n\nfragment ClapMutation_post on Post {\n  __typename\n  id\n  clapCount\n  ...MultiVoteCount_post\n}\n\nfragment ExplicitSignalMenuOptions_post on Post {\n  ...NegativeSignalModal_post\n  __typename\n  id\n}\n\nfragment NegativeSignalModal_post on Post {\n  id\n  creator {\n    ...NegativeSignalModal_publisher\n    viewerEdge {\n      id\n      isMuting\n      __typename\n    }\n    __typename\n    id\n  }\n  collection {\n    ...NegativeSignalModal_publisher\n    viewerEdge {\n      id\n      isMuting\n      __typename\n    }\n    __typename\n    id\n  }\n  __typename\n}\n\nfragment NegativeSignalModal_publisher on Publisher {\n  __typename\n  id\n  name\n}\n\nfragment PostPreviewFooterMeta_post on Post {\n  isLocked\n  postResponses {\n    count\n    __typename\n  }\n  ...usePostPublishedAt_post\n  ...Star_post\n  __typename\n  id\n}\n\nfragment usePostPublishedAt_post on Post {\n  firstPublishedAt\n  latestPublishedAt\n  pinnedAt\n  __typename\n  id\n}\n\nfragment Star_post on Post {\n  id\n  creator {\n    id\n    __typename\n  }\n  isLocked\n  __typename\n}\n\nfragment PostPreviewByLine_post on Post {\n  creator {\n    ...PostPreviewByLineAuthor_user\n    __typename\n    id\n  }\n  collection {\n    ...PostPreviewByLineCollection_collection\n    __typename\n    id\n  }\n  __typename\n  id\n}\n\nfragment PostPreviewByLineAuthor_user on User {\n  ...UserMentionTooltip_user\n  ...UserAvatar_user\n  ...UserName_user\n  __typename\n  id\n}\n\nfragment UserMentionTooltip_user on User {\n  id\n  name\n  bio\n  ...UserAvatar_user\n  ...UserFollowButton_user\n  ...useIsVerifiedBookAuthor_user\n  __typename\n}\n\nfragment UserName_user on User {\n  name\n  ...useIsVerifiedBookAuthor_user\n  ...userUrl_user\n  ...UserMentionTooltip_user\n  __typename\n  id\n}\n\nfragment PostPreviewByLineCollection_collection on Collection {\n  ...CollectionAvatar_collection\n  ...CollectionTooltip_collection\n  ...CollectionLinkWithPopover_collection\n  __typename\n  id\n}\n\nfragment CollectionTooltip_collection on Collection {\n  id\n  name\n  slug\n  description\n  subscriberCount\n  customStyleSheet {\n    header {\n      backgroundImage {\n        id\n        __typename\n      }\n      __typename\n    }\n    __typename\n    id\n  }\n  ...CollectionAvatar_collection\n  ...CollectionFollowButton_collection\n  ...EntityPresentationRankedModulePublishingTracker_entity\n  __typename\n}\n\nfragment EntityPresentationRankedModulePublishingTracker_entity on RankedModulePublishingEntity {\n  __typename\n  ... on Collection {\n    id\n    __typename\n  }\n  ... on User {\n    id\n    __typename\n  }\n}\n\nfragment CollectionLinkWithPopover_collection on Collection {\n  name\n  ...collectionUrl_collection\n  ...CollectionTooltip_collection\n  __typename\n  id\n}\n\nfragment PostPreviewInformation_post on Post {\n  readingTime\n  isLocked\n  ...Star_post\n  ...usePostPublishedAt_post\n  __typename\n  id\n}\n\nfragment PostPreviewContainer_post on Post {\n  id\n  extendedPreviewContent {\n    isFullContent\n    __typename\n  }\n  visibility\n  pinnedAt\n  ...PostScrollTracker_post\n  ...usePostUrl_post\n  __typename\n}\n\nfragment PostScrollTracker_post on Post {\n  id\n  collection {\n    id\n    __typename\n  }\n  sequence {\n    sequenceId\n    __typename\n  }\n  __typename\n}\n\nfragment usePostUrl_post on Post {\n  id\n  creator {\n    ...userUrl_user\n    __typename\n    id\n  }\n  collection {\n    id\n    domain\n    slug\n    __typename\n  }\n  isSeries\n  mediumUrl\n  sequence {\n    slug\n    __typename\n  }\n  uniqueSlug\n  __typename\n}\n\nfragment NewsletterV3Promo_publisher on Publisher {\n  __typename\n  ... on User {\n    ...NewsletterV3Promo_user\n    __typename\n    id\n  }\n  ... on Collection {\n    ...NewsletterV3Promo_collection\n    __typename\n    id\n  }\n}\n\nfragment NewsletterV3Promo_user on User {\n  id\n  username\n  name\n  viewerEdge {\n    isUser\n    __typename\n    id\n  }\n  newsletterV3 {\n    id\n    ...NewsletterV3Promo_newsletterV3\n    __typename\n  }\n  __typename\n}\n\nfragment NewsletterV3Promo_newsletterV3 on NewsletterV3 {\n  slug\n  name\n  description\n  promoHeadline\n  promoBody\n  ...NewsletterSubscribeComponent_newsletterV3\n  __typename\n  id\n}\n\nfragment NewsletterSubscribeComponent_newsletterV3 on NewsletterV3 {\n  ...NewsletterV3SubscribeButton_newsletterV3\n  ...NewsletterV3SubscribeByEmail_newsletterV3\n  __typename\n  id\n}\n\nfragment NewsletterV3SubscribeButton_newsletterV3 on NewsletterV3 {\n  id\n  name\n  slug\n  type\n  user {\n    id\n    name\n    username\n    __typename\n  }\n  collection {\n    slug\n    ...SusiClickable_collection\n    ...collectionDefaultBackgroundTheme_collection\n    __typename\n    id\n  }\n  ...SusiClickable_newsletterV3\n  ...useNewsletterV3Subscription_newsletterV3\n  __typename\n}\n\nfragment collectionDefaultBackgroundTheme_collection on Collection {\n  colorPalette {\n    ...collectionDefaultBackgroundTheme_colorPalette\n    __typename\n  }\n  customStyleSheet {\n    id\n    ...collectionDefaultBackgroundTheme_customStyleSheet\n    __typename\n  }\n  __typename\n  id\n}\n\nfragment collectionDefaultBackgroundTheme_colorPalette on ColorPalette {\n  ...customDefaultBackgroundTheme_colorPalette\n  __typename\n}\n\nfragment customDefaultBackgroundTheme_colorPalette on ColorPalette {\n  highlightSpectrum {\n    ...ThemeUtil_colorSpectrum\n    __typename\n  }\n  defaultBackgroundSpectrum {\n    ...ThemeUtil_colorSpectrum\n    __typename\n  }\n  tintBackgroundSpectrum {\n    ...ThemeUtil_colorSpectrum\n    __typename\n  }\n  __typename\n}\n\nfragment collectionDefaultBackgroundTheme_customStyleSheet on CustomStyleSheet {\n  id\n  ...customDefaultBackgroundTheme_customStyleSheet\n  __typename\n}\n\nfragment customDefaultBackgroundTheme_customStyleSheet on CustomStyleSheet {\n  id\n  global {\n    colorPalette {\n      primary {\n        colorPalette {\n          ...customDefaultBackgroundTheme_colorPalette\n          __typename\n        }\n        __typename\n      }\n      background {\n        colorPalette {\n          ...customDefaultBackgroundTheme_colorPalette\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment SusiClickable_newsletterV3 on NewsletterV3 {\n  ...SusiContainer_newsletterV3\n  __typename\n  id\n}\n\nfragment SusiContainer_newsletterV3 on NewsletterV3 {\n  ...SignInOptions_newsletterV3\n  ...SignUpOptions_newsletterV3\n  __typename\n  id\n}\n\nfragment SignInOptions_newsletterV3 on NewsletterV3 {\n  id\n  name\n  __typename\n}\n\nfragment SignUpOptions_newsletterV3 on NewsletterV3 {\n  id\n  name\n  __typename\n}\n\nfragment NewsletterV3SubscribeByEmail_newsletterV3 on NewsletterV3 {\n  id\n  slug\n  type\n  user {\n    id\n    name\n    username\n    __typename\n  }\n  collection {\n    ...collectionDefaultBackgroundTheme_collection\n    ...collectionUrl_collection\n    __typename\n    id\n  }\n  __typename\n}\n\nfragment NewsletterV3Promo_collection on Collection {\n  id\n  slug\n  domain\n  name\n  newsletterV3 {\n    id\n    ...NewsletterV3Promo_newsletterV3\n    __typename\n  }\n  __typename\n}\n\nfragment PublisherHomepagePosts_user on User {\n  id\n  ...useShowAuthorNewsletterV3Promo_user\n  __typename\n}\n\nfragment useShowAuthorNewsletterV3Promo_user on User {\n  id\n  username\n  newsletterV3 {\n    id\n    showPromo\n    slug\n    __typename\n  }\n  __typename\n}\n\nfragment UserProfileMetadata_user on User {\n  id\n  username\n  name\n  bio\n  socialStats {\n    followerCount\n    followingCount\n    __typename\n  }\n  ...userUrl_user\n  ...UserProfileMetadataHelmet_user\n  __typename\n}\n\nfragment UserProfileMetadataHelmet_user on User {\n  username\n  name\n  imageId\n  twitterScreenName\n  navItems {\n    title\n    __typename\n  }\n  __typename\n  id\n}\n\nfragment SuspendedBannerLoader_user on User {\n  id\n  isSuspended\n  __typename\n}\n\nfragment useAnalytics_user on User {\n  id\n  imageId\n  name\n  username\n  __typename\n}\n\nfragment UserProfileBooks_user on User {\n  username\n  authoredBooks {\n    ...BookWidget_authorBook\n    __typename\n  }\n  __typename\n  id\n}\n\nfragment BookWidget_authorBook on AuthorBook {\n  authors {\n    name\n    user {\n      id\n      __typename\n    }\n    __typename\n  }\n  description\n  title\n  links {\n    title\n    url\n    __typename\n  }\n  publicationDate\n  ...BookCover_authorBook\n  __typename\n}\n\nfragment BookCover_authorBook on AuthorBook {\n  coverImageId\n  __typename\n}\n"
            }]

            response = self.__make_http_request(url, "POST", payload)
            if not response:
                return [], None

            response_data = response.json()[0]
            user_result = response_data.get('data', {}).get('userResult', {})
            posts_connection = user_result.get('homepagePostsConnection', {})
            
            # Extract next page token
            paging_info = posts_connection.get('pagingInfo', {}).get('next')
            next_token = paging_info.get('from') if paging_info else None

            # Parse articles
            articles = []
            for post in posts_connection.get('posts', []):
                article = self.__parse_article_data(post, isHomePage=False)
                if article:
                    articles.append(article)

            return articles, next_token

        except Exception as e:
            print(f"Error fetching more articles: {e}")
            return [], None
        
    def get_user_articles(self, username: str, page_token: Optional[str] = None) -> Tuple[List[Dict], Optional[str]]:
        """
        Get list of articles for a Medium user.
        
        Args:
            username: Medium username without @ symbol
            page_token: Optional pagination token for fetching next page
            
        Returns:
            Tuple containing:
            - List of article metadata dictionaries
            - Next page token (if more articles exist)
            
        Raises:
            MediumProfileError: If username is invalid or profile not found
        """
        if not username:
            raise MediumProfileError("Username is required")

        username = username.strip().lstrip('@')
        
        try:
            if page_token:
                return self.__fetch_more_articles(username, page_token)
            return self.__fetch_initial_articles(username)
            
        except Exception as e:
            return [], None