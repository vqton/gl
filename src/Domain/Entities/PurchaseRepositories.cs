using System;
using System.Collections.Generic;

namespace GL.Domain.Entities
{
    public interface IPurchaseRepository
    {
        void Add(PurchaseTransaction purchase);
        PurchaseTransaction GetById(string id);
        List<PurchaseTransaction> GetAll();
    }

    public class InMemoryPurchaseRepository : IPurchaseRepository
    {
        private readonly List<PurchaseTransaction> _purchases = new();

        public void Add(PurchaseTransaction purchase)
        {
            _purchases.Add(purchase);
        }

        public PurchaseTransaction GetById(string id)
        {
            return _purchases.Find(p => p.Id == id);
        }

        public List<PurchaseTransaction> GetAll()
        {
            return _purchases;
        }
    }
}