<%@ Page Inherits="Microsoft.SharePoint.Publishing.TemplateRedirectionPage,Microsoft.SharePoint.Publishing,Version=16.0.0.0,Culture=neutral,PublicKeyToken=71e9bce111e9429c" %> <%@ Reference VirtualPath="~TemplatePageUrl" %> <%@ Reference VirtualPath="~masterurl/custom.master" %><%@ Register Tagprefix="SharePoint" Namespace="Microsoft.SharePoint.WebControls" Assembly="Microsoft.SharePoint, Version=16.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c" %>
<html xmlns:mso="urn:schemas-microsoft-com:office:office" xmlns:msdt="uuid:C2F41010-65B3-11d1-A29F-00AA00C14882"><head>
<!--[if gte mso 9]><SharePoint:CTFieldRefs runat=server Prefix="mso:" FieldList="FileLeafRef,Comments,PublishingStartDate,PublishingExpirationDate,PublishingContactEmail,PublishingContactName,PublishingContactPicture,PublishingPageLayout,PublishingVariationGroupID,PublishingVariationRelationshipLinkFieldID,PublishingRollupImage,Audience,PublishingIsFurlPage,PublishingPageImage,PublishingPageContent,SummaryLinks,ArticleByLine,ArticleStartDate,PublishingImageCaption,HeaderStyleDefinitions"><xml>
<mso:CustomDocumentProperties>
<mso:PublishingContact msdt:dt="string">10</mso:PublishingContact>
<mso:PublishingIsFurlPage msdt:dt="string">0</mso:PublishingIsFurlPage>
<mso:display_urn_x003a_schemas-microsoft-com_x003a_office_x003a_office_x0023_PublishingContact msdt:dt="string">Samuel Marçal</mso:display_urn_x003a_schemas-microsoft-com_x003a_office_x003a_office_x0023_PublishingContact>
<mso:PublishingContactPicture msdt:dt="string"></mso:PublishingContactPicture>
<mso:PublishingContactName msdt:dt="string"></mso:PublishingContactName>
<mso:ContentTypeId msdt:dt="string">0x010100C568DB52D9D0A14D9B2FDCC96666E9F2007948130EC3DB064584E219954237AF3900242457EFB8B24247815D688C526CD44D0096CB112DF87E2F45AFEB8B21D0660412</mso:ContentTypeId>
<mso:PublishingPageLayoutName msdt:dt="string">PageFromDocLayout.aspx</mso:PublishingPageLayoutName>
<mso:Comments msdt:dt="string"></mso:Comments>
<mso:PublishingContactEmail msdt:dt="string"></mso:PublishingContactEmail>
<mso:PublishingPageLayout msdt:dt="string">https://sharepointtestfreetrial.sharepoint.com/sites/ImeaExample%E2%80%8ESite/_catalogs/masterpage/PageFromDocLayout.aspx, Body only</mso:PublishingPageLayout>
<mso:PublishingPageContent msdt:dt="string">
{page_content}
</mso:PublishingPageContent>
<mso:PublishingRollupImage msdt:dt="string"></mso:PublishingRollupImage>
</mso:CustomDocumentProperties>
</xml></SharePoint:CTFieldRefs><![endif]-->
<title>{page_title}</title></head>