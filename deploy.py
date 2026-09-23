import argparse
import sys
from azure.identity import InteractiveBrowserCredential
from fabric_cicd import FabricWorkspace, publish_all_items, append_feature_flag

def deploy_to_fabric(workspace: str, folder: str = None, environment: str = "dev"):
    """
    Local PBIP projesini Microsoft Fabric Workspace'ine deploy eder.
    """
    target_info = f"'{workspace}'" + (f" / '{folder}' klasörü" if folder else "")
    print(f"🚀 Deploy işlemi başlatılıyor: {target_info} ({environment} ortamı)...")

    try:
        # 1. Feature Flag'leri FabricWorkspace oluşturulmadan ÖNCE modül seviyesinde ekliyoruz
        append_feature_flag("enable_experimental_features")
        append_feature_flag("enable_include_folder")

        # 2. Kimlik Doğrulama
        credential = InteractiveBrowserCredential()

        # 3. FabricWorkspace Nesnesinin Oluşturulması
        ws = FabricWorkspace(
            workspace_name=workspace,
            environment=environment,
            repository_directory=".",
            item_type_in_scope=["SemanticModel", "Report"],
            token_credential=credential
        )

        # 4. Klasör Filtresinin Ayarlanması (Yol '/' ile başlamalıdır)
        folder_include = [f"/{folder}"] if folder else None

        # 5. Yayınlama İşleminin Başlatılması
        publish_all_items(
            fabric_workspace_obj=ws,
            folder_path_to_include=folder_include
        )
        
        print(f"✅ Deploy işlemi başarıyla tamamlandı: {target_info}")

    except Exception as e:
        print(f"❌ Deploy sırasında bir hata oluştu: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Power BI PBIP Fabric Deployment Script")
    parser.add_argument("--workspace", "--workspace_name", type=str, required=True, help="Hedef Fabric Workspace adı")
    parser.add_argument("--folder", "--folder_name", type=str, default=None, help="Opsiyonel: Repo içindeki filtrelenecek alt klasör")
    parser.add_argument("--env", type=str, default="dev", help="Ortam adı (dev, test, prod)")
    
    args = parser.parse_args()
    deploy_to_fabric(
        workspace=args.workspace, 
        folder=args.folder, 
        environment=args.env
    )